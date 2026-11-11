"""Settle completed bicycle rentals with the payment processor."""
from urbanmesh.application.ports import RideRepository, FarePolicy
from urbanmesh.infrastructure.gateways.payments import ProcessorPaymentAdapter
from urbanmesh.domain.errors import NotFound

class SettlementService:
    def __init__(self, rides: RideRepository, fares: FarePolicy,
                 processor: ProcessorPaymentAdapter):
        self.rides, self.fares, self.processor = rides, fares, processor

    def settle(self, ride_id: str) -> str:
        ride = self.rides.find(ride_id)
        if ride is None: raise NotFound("ride not found")
        if ride.ended_at is None: raise ValueError("ride incomplete")
        quote = self.fares.quote(ride)
        response = self.processor.capture(quote)
        if not response["paid"]: raise RuntimeError("processor declined")
        return response["id"]
