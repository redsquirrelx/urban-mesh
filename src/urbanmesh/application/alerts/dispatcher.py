"""Distribute disruption notices to subscribed passengers."""
from datetime import date
from urbanmesh.application.ports import MessageGateway, RepairQueue
from urbanmesh.domain.models import Disruption, RepairTicket

class AlertDispatcher:
    def __init__(self, messages: MessageGateway, work_orders: RepairQueue):
        self.messages, self.work_orders = messages, work_orders

    def dispatch(self, event: Disruption, subscriptions: dict[str,set[str]]) -> int:
        text = f"Service advisory for {event.route_id}: {event.reason}"
        count = 0
        for rider_id, route_ids in subscriptions.items():
            if event.route_id in route_ids:
                self.messages.send(rider_id, text)
                count += 1
        if event.severity in {"high", "critical"}:
            self.work_orders.enqueue(RepairTicket(event.vehicle_id, event.reason,
                                                "urgent", date.today()))
        return count
