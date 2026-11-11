"""Passenger fare quotation using route data and pricing rules."""
from urbanmesh.application.ports import RouteSource, AuditSink
from urbanmesh.domain.models import FareQuote
from urbanmesh.domain.policies.pricing import bus_fare

class FareQuoteService:
    def __init__(self, routes: RouteSource, audits: AuditSink):
        self.routes, self.audits = routes, audits

    def quote(self, route_id: str, rider_id: str, peak: bool = False,
              concession: bool = False) -> FareQuote:
        if not rider_id.strip(): raise ValueError("rider required")
        route = self.routes.get(route_id)
        if route is None: raise KeyError(route_id)
        fare = FareQuote(route_id, rider_id, bus_fare(route.base_fare_cents, peak, concession))
        self.audits.append({"kind": "fare_regulatory_assessment", "rider": rider_id,
                            "route": route_id, "concession": concession, "peak": peak})
        return fare
