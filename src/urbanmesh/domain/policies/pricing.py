"""Pricing calculations in integer minor currency units."""
from math import ceil
from urbanmesh.domain.models import Ride, FareQuote


def bus_fare(base_cents: int, peak: bool, concession: bool) -> int:
    if base_cents < 0:
        raise ValueError("base fare must be nonnegative")
    amount = base_cents + (75 if peak else 0)
    return max(0, amount - (90 if concession else 0))

class FlatFarePolicy:
    def __init__(self, cents: int = 250): self.cents = cents
    def quote(self, ride: Ride) -> FareQuote:
        return FareQuote(ride.ride_id, ride.rider_id, self.cents)

class MinuteFarePolicy:
    def __init__(self, unlock_cents: int = 100, minute_cents: int = 20):
        self.unlock_cents, self.minute_cents = unlock_cents, minute_cents

    def quote(self, ride: Ride) -> FareQuote:
        if ride.ended_at is None: raise ValueError("ride not completed")
        minutes = max(1, int((ride.ended_at - ride.started_at).total_seconds() / 60))
        return FareQuote(ride.ride_id, ride.rider_id, self.unlock_cents + minutes * self.minute_cents)

class PromotionalFarePolicy:
    def __init__(self, discount_cents: int = 50): self.discount_cents = discount_cents
    def quote(self, ride: Ride) -> FareQuote:
        return FareQuote(ride.ride_id, ride.rider_id, -self.discount_cents)
