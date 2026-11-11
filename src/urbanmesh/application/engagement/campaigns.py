"""Passenger engagement campaign scheduling."""
from urbanmesh.application.ports import CampaignQueue
from urbanmesh.application.engagement.offers import ticket_offer
class CampaignService:
    def __init__(self, queue: CampaignQueue): self.queue = queue
    def schedule(self, rider_id: str, rides_last_month: int) -> str | None:
        offer = ticket_offer(rides_last_month)
        if offer: self.queue.enqueue(rider_id,offer)
        return offer
