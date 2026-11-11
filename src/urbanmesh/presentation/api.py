"""HTTP endpoints for public transit, rentals and depot operations."""
from dataclasses import asdict
from datetime import date, datetime, timezone
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from urbanmesh.bootstrap import build_services, Services
from urbanmesh.domain.errors import DomainError, NotFound, Conflict, InvalidRequest
from urbanmesh.domain.models import (StockItem,PurchaseLine,Rider,Disruption,
                                     CustodyEvent,SupplyOrder)
from urbanmesh.domain.policies.validation import validate_password
from urbanmesh.application.procurement.preview import preview_discount
from urbanmesh.application.procurement.quote import SupplyQuoteRequest
from urbanmesh.domain.policies.shipping import DeliveryZone
from urbanmesh.presentation.admin import low_stock_skus
from urbanmesh.application.telemetry.exceptions import QualityExceptionLedger

class StockCreate(BaseModel):
    sku: str; name: str; price_cents: int; stock: int; ratings: list[float] = []
class StockUpdate(BaseModel): stock: int
class PurchaseLineRequest(BaseModel): sku: str; quantity: int
class PurchaseRequest(BaseModel): lines: list[PurchaseLineRequest]
class PasswordRequest(BaseModel): password: object
class RiderCreate(BaseModel): rider_id: str; email: str
class RouteQuoteRequest(BaseModel): route_id: str; rider_id: str; peak: bool = False; concession: bool = False
class JourneyRequest(BaseModel):
    origin: str; destination: str; rider_id: str; rides_last_month: int = 0
    travel_day: date
class TicketIssueRequest(BaseModel): route_id: str; rider_id: str; rides_last_month: int = 0
class RideStartRequest(BaseModel):
    ride_id: str; rider_id: str; bike_id: str; started_at: datetime
class RideFinishRequest(BaseModel): ended_at: datetime
class DisruptionRequest(BaseModel): route_id: str; vehicle_id: str; reason: str; severity: str
class MaintenanceRequest(BaseModel): asset_id: str; description: str; priority: str = "normal"
class CheckoutRequest(BaseModel): order_id: str; sku: str; quantity: int; unit_price_cents: int
class CustodyRequest(BaseModel): sensor_id: str; action: str; actor: str; recorded_on: date
class SupplyQuotePayload(BaseModel):
    sku: str; quantity: int; zone: DeliveryZone; promotion_code: str | None = None


def create_app(services: Services | None = None) -> FastAPI:
    app = FastAPI(title="UrbanMesh Mobility Operations", version="1.4.0")
    svc = services or build_services()
    app.state.services = svc

    @app.exception_handler(DomainError)
    async def domain_error_handler(request, exc):
        from fastapi.responses import JSONResponse
        status = 404 if isinstance(exc,NotFound) else 409 if isinstance(exc,Conflict) else 422
        return JSONResponse(status_code=status, content={"detail":str(exc)})

    @app.get("/health")
    def health(): return {"status":"ok"}

    @app.get("/routes")
    def list_routes(): return [asdict(x) for x in svc.routes_store.all_routes()]

    @app.get("/routes/{route_id}")
    def get_route(route_id: str):
        item = svc.routes_store.get(route_id)
        if item is None: raise HTTPException(404,"route not found")
        return asdict(item)

    @app.post("/journeys/search")
    def search_journeys(payload: JourneyRequest):
        try: return [asdict(x) for x in svc.journeys.plan(**payload.model_dump())]
        except ValueError as exc: raise HTTPException(422,str(exc))

    @app.post("/fares/quote")
    def quote_fare(payload: RouteQuoteRequest):
        try: return asdict(svc.fares.quote(**payload.model_dump()))
        except KeyError: raise HTTPException(404,"route not found")
        except ValueError as exc: raise HTTPException(422,str(exc))

    @app.post("/tickets", status_code=201)
    def issue_ticket(payload: TicketIssueRequest):
        try: fare = svc.fares.quote(payload.route_id,payload.rider_id)
        except KeyError: raise HTTPException(404,"route not found")
        return asdict(svc.tickets.issue(fare,payload.rides_last_month))

    @app.get("/tickets/{ticket_id}")
    def get_ticket(ticket_id: str):
        item = svc.ticket_store.find(ticket_id)
        if item is None: raise HTTPException(404,"ticket not found")
        return asdict(item)

    @app.get("/stations/{station_id}/bicycles")
    def available_bikes(station_id: str): return [asdict(x) for x in svc.bikes_store.available_at(station_id)]

    @app.post("/rides", status_code=201)
    def start_ride(payload: RideStartRequest): return asdict(svc.rides.start(payload.ride_id,payload.rider_id,payload.bike_id,payload.started_at))

    @app.get("/rides/{ride_id}")
    def get_ride(ride_id: str):
        item=svc.rides_store.find(ride_id)
        if item is None: raise HTTPException(404,"ride not found")
        return asdict(item)

    @app.patch("/rides/{ride_id}/finish")
    def finish_ride(ride_id: str, payload: RideFinishRequest):
        return asdict(svc.rides.finish(ride_id,payload.ended_at))

    @app.post("/rides/{ride_id}/settle")
    def settle_ride(ride_id: str):
        try: return {"receipt_reference":svc.payments.settle(ride_id)}
        except ValueError as exc: raise HTTPException(422,str(exc))

    @app.get("/stops/{stop_id}/departures")
    def departures(stop_id: str, minute: int = 0, driver_id: str = "", hours_on_duty: float = 0.0):
        try: return svc.boards.build(stop_id,minute,driver_id,hours_on_duty)
        except ValueError as exc: raise HTTPException(422,str(exc))

    @app.post("/alerts/disruptions")
    def send_alert(payload: DisruptionRequest):
        subscribers={"u-001":{"R-01","R-02"},"u-002":{"R-03"}}
        return {"recipients": svc.alerts.dispatch(Disruption(**payload.model_dump()),subscribers)}

    @app.get("/reports/ridership")
    def ridership(as_of: date): return svc.ridership.build(as_of)

    @app.post("/maintenance/work-orders", status_code=201)
    def report_maintenance(payload: MaintenanceRequest):
        return asdict(svc.maintenance.report(**payload.model_dump()))

    @app.get("/maintenance/work-orders")
    def list_maintenance(): return [asdict(x) for x in svc.repairs_store.list_all()]

    @app.get("/telemetry/sensors/{sensor_id}")
    def read_sensor(sensor_id: str): return asdict(svc.telemetry.process(sensor_id))

    @app.post("/telemetry/sensors/{sensor_id}/assess")
    def assess_sensor(sensor_id: str):
        reading=svc.telemetry.process(sensor_id)
        return asdict(svc.quality.review(reading))

    @app.get("/telemetry/quality/{sensor_id}")
    def get_quality(sensor_id: str):
        result=svc.quality_store.find(sensor_id)
        if result is None: raise HTTPException(404,"result not found")
        return asdict(result)

    @app.get("/telemetry/exceptions")
    def quality_exceptions(operator: str | None = None):
        return [asdict(x) for x in QualityExceptionLedger(svc.quality_store).pending(operator)]

    @app.post("/telemetry/custody", status_code=201)
    def add_custody(payload: CustodyRequest):
        svc.custody.record(CustodyEvent(**payload.model_dump()))
        return {"recorded": True}

    @app.get("/telemetry/custody/export")
    def export_custody(): return {"rows":svc.custody.export_csv()}

    @app.get("/reports/telemetry")
    def report_telemetry(as_of: date): return {"older_records":svc.telemetry_report.count_old_records(as_of)}

    @app.post("/operations/retention/run")
    def retention(as_of: date, days: int = 180):
        try: return {"deleted":svc.retention.prune(as_of,days)}
        except ValueError as exc: raise HTTPException(422,str(exc))

    @app.get("/inventory")
    def list_stock(): return [asdict(x) for x in svc.inventory.list()]

    @app.get("/inventory/{sku}")
    def get_stock(sku: str): return asdict(svc.inventory.get(sku))

    @app.post("/inventory",status_code=201)
    def create_stock(payload: StockCreate):
        return asdict(svc.inventory.create(StockItem(**payload.model_dump())))

    @app.patch("/inventory/{sku}/stock")
    def update_stock(sku: str,payload: StockUpdate):
        return asdict(svc.inventory.update_stock(sku,payload.stock))

    @app.delete("/inventory/{sku}",status_code=204)
    def delete_stock(sku: str):
        svc.inventory.delete(sku)
        return Response(status_code=204)

    @app.get("/inventory/{sku}/average-rating")
    def average_rating(sku: str): return {"average":svc.inventory.average_rating(sku)}

    @app.post("/purchases/total")
    def purchase_total(payload: PurchaseRequest):
        lines=[PurchaseLine(**x.model_dump()) for x in payload.lines]
        return {"total_cents":svc.inventory.purchase_total(lines)}

    @app.post("/procurement/quotes",status_code=201)
    def make_supply_quote(payload: SupplyQuotePayload):
        return asdict(svc.supply_quotes.quote(SupplyQuoteRequest(**payload.model_dump())))

    @app.get("/procurement/quotes/{quote_id}")
    def get_supply_quote(quote_id: str):
        return asdict(svc.supply_quotes.get(quote_id))

    @app.post("/procurement/checkout", status_code=201)
    def checkout(payload: CheckoutRequest):
        return {"receipt_reference":svc.checkout.checkout(SupplyOrder(**payload.model_dump()))}

    @app.get("/procurement/discount-preview")
    def discount_preview(code: str, subtotal_cents: int):
        return {"discount_cents":preview_discount(code,subtotal_cents)}

    @app.get("/admin/low-stock")
    def low_stock(threshold: int = 4): return {"skus":low_stock_skus(svc.inventory_store,threshold)}

    @app.post("/passwords/validate")
    def password_check(payload: PasswordRequest): return {"valid":validate_password(payload.password)}

    @app.get("/riders")
    def list_riders(): return [asdict(x) for x in svc.accounts.list()]

    @app.get("/riders/{rider_id}")
    def get_rider(rider_id: str): return asdict(svc.accounts.get(rider_id))

    @app.post("/riders", status_code=201)
    def add_rider(payload: RiderCreate):
        return asdict(svc.accounts.register(Rider(**payload.model_dump())))

    return app

app = create_app()
