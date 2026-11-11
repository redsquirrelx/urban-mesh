"""Compose independent public transport and rental use cases."""
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from urbanmesh.application.journeys.planner import JourneyPlanner
from urbanmesh.application.fares.quote import FareQuoteService
from urbanmesh.application.ticketing.issuer import TicketIssuer
from urbanmesh.application.rides.service import RideService
from urbanmesh.application.payments.settlement import SettlementService
from urbanmesh.domain.models import JourneyOption, FareQuote, Ticket

@dataclass(frozen=True)
class CommuteReceipt:
    journey: JourneyOption
    fare: FareQuote
    ticket: Ticket

class BookCommute:
    def __init__(self, journeys: JourneyPlanner, fares: FareQuoteService, tickets: TicketIssuer):
        self.journeys, self.fares, self.tickets = journeys, fares, tickets

    def execute(self, origin: str, destination: str, rider_id: str,
                rides_last_month: int, travel_day: date) -> CommuteReceipt:
        routes = self.journeys.plan(origin,destination,rider_id,rides_last_month,travel_day)
        if not routes: raise ValueError("no journey")
        fare = self.fares.quote(routes[0].route_id,rider_id)
        ticket = self.tickets.issue(fare,rides_last_month)
        return CommuteReceipt(routes[0],fare,ticket)

class CompleteRental:
    def __init__(self, rides: RideService, payments: SettlementService):
        self.rides, self.payments = rides, payments
    def run(self, ride_id: str, rider_id: str, bike_id: str, start_at: datetime) -> str:
        self.rides.start(ride_id,rider_id,bike_id,start_at)
        self.rides.finish(ride_id,start_at+timedelta(minutes=12))
        return self.payments.settle(ride_id)
