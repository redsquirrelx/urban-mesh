"""Issue a confirmed passenger ticket."""
from datetime import date
from urbanmesh.application.ports import TicketStore, CampaignQueue
from urbanmesh.domain.models import FareQuote, Ticket
from urbanmesh.application.engagement.offers import ticket_offer

class TicketIssuer:
    def __init__(self, tickets: TicketStore, campaigns: CampaignQueue):
        self.tickets, self.campaigns = tickets, campaigns

    def issue(self, fare: FareQuote, rides_last_month: int = 0) -> Ticket:
        ticket = Ticket(f"T-{fare.rider_id}-{fare.reference_id}", fare.reference_id,
                        fare.rider_id, fare.amount_cents, date.today())
        self.tickets.save(ticket)
        offer = ticket_offer(rides_last_month)
        if offer: self.campaigns.enqueue(fare.rider_id, offer)
        return ticket
