"""Process-local adapters for local deployment and smoke tests."""
from dataclasses import replace
from datetime import date
from urbanmesh.domain.models import (Route, Bicycle, Ride, Ticket, RepairTicket,
    Boarding, SensorReading, QualityResult, StockItem, CustodyEvent, SupplyOrder)

class MemoryRouteSource:
    def __init__(self, routes: list[Route]): self._routes = {r.route_id:r for r in routes}
    def get(self, route_id: str) -> Route | None: return self._routes.get(route_id)
    def all_routes(self) -> list[Route]: return list(self._routes.values())
    def connecting(self, origin: str, destination: str) -> list[tuple[Route,int]]:
        found = []
        for route in self._routes.values():
            if origin in route.stops and destination in route.stops:
                a, b = route.stops.index(origin), route.stops.index(destination)
                if a < b: found.append((route, sum(route.hop_minutes[a:b])))
        return found

class MemoryBikeCatalog:
    def __init__(self, bikes: list[Bicycle]): self._bikes = {b.bike_id:b for b in bikes}
    def find(self, bike_id: str) -> Bicycle | None: return self._bikes.get(bike_id)
    def available_at(self, station_id: str) -> list[Bicycle]:
        return [b for b in self._bikes.values() if b.station_id == station_id and b.operational]
    def set_operational(self, bike_id: str, operational: bool) -> None:
        bike = self._bikes[bike_id]
        self._bikes[bike_id] = replace(bike, operational=operational)

class MemoryRideRepository:
    def __init__(self): self._rides: dict[str,Ride] = {}
    def save(self, ride: Ride) -> None: self._rides[ride.ride_id] = ride
    def find(self, ride_id: str) -> Ride | None: return self._rides.get(ride_id)
    def list_all(self) -> list[Ride]: return list(self._rides.values())

class MemoryTicketStore:
    def __init__(self): self._tickets: dict[str,Ticket] = {}
    def save(self, ticket: Ticket) -> None: self._tickets[ticket.ticket_id] = ticket
    def find(self, ticket_id: str) -> Ticket | None: return self._tickets.get(ticket_id)

class MemoryAuditSink:
    def __init__(self): self.events: list[dict] = []
    def append(self, event: dict) -> None: self.events.append(dict(event))

class MemoryCampaignQueue:
    def __init__(self): self.entries: list[tuple[str,str]] = []
    def enqueue(self, rider_id: str, offer_code: str) -> None:
        self.entries.append((rider_id, offer_code))

class MemoryMessages:
    def __init__(self): self.sent: list[tuple[str,str]] = []
    def send(self, recipient: str, text: str) -> None: self.sent.append((recipient,text))

class MemoryRepairQueue:
    def __init__(self): self.tickets: list[RepairTicket] = []
    def enqueue(self, ticket: RepairTicket) -> None: self.tickets.append(ticket)
    def list_all(self) -> list[RepairTicket]: return list(self.tickets)

class MemoryBoardingStore:
    def __init__(self, records: list[Boarding]): self._records = list(records)
    def read_all(self) -> list[Boarding]: return list(self._records)
    def delete_before(self, cutoff: date) -> int:
        before = len(self._records)
        self._records = [r for r in self._records if r.boarded_on >= cutoff]
        return before - len(self._records)

class MemoryShiftFlags:
    def __init__(self): self.entries: list[tuple[str,str]] = []
    def flag(self, driver_id: str, status: str) -> None: self.entries.append((driver_id,status))

class MemoryQualityStore:
    def __init__(self): self._results: dict[str,QualityResult] = {}
    def save(self, result: QualityResult) -> None: self._results[result.sensor_id] = result
    def find(self, sensor_id: str) -> QualityResult | None: return self._results.get(sensor_id)
    def list_all(self) -> list[QualityResult]: return list(self._results.values())

class MemoryCustodySink:
    def __init__(self): self.events: list[CustodyEvent] = []
    def append(self, event: CustodyEvent) -> None: self.events.append(event)
    def list_events(self) -> list[CustodyEvent]: return list(self.events)

class MemoryTelemetryStore:
    def __init__(self, readings: list[SensorReading]): self._readings = list(readings)
    def add(self, reading: SensorReading) -> None: self._readings.append(reading)
    def list_before(self, cutoff: date) -> list[SensorReading]:
        return [x for x in self._readings if x.captured_at.date() < cutoff]
    def delete_before(self, cutoff: date) -> int:
        before = len(self._readings)
        self._readings = [x for x in self._readings if x.captured_at.date() >= cutoff]
        return before - len(self._readings)
    def list_all(self) -> list[SensorReading]: return list(self._readings)

class MemoryInventoryCatalog:
    def __init__(self, items: list[StockItem]): self._items = {x.sku:x for x in items}
    def list_items(self) -> list[StockItem]: return list(self._items.values())
    def find(self, sku: str) -> StockItem | None: return self._items.get(sku)
    def save(self, item: StockItem) -> None: self._items[item.sku] = item
    def remove(self, sku: str) -> bool: return self._items.pop(sku,None) is not None

class MemorySupplyOrders:
    def __init__(self): self._orders: dict[str,SupplyOrder] = {}
    def save(self, order: SupplyOrder) -> None: self._orders[order.order_id] = order
    def find(self, order_id: str) -> SupplyOrder | None: return self._orders.get(order_id)
    def list_all(self) -> list[SupplyOrder]: return list(self._orders.values())
