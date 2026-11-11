"""Independent fleet maintenance priority decisions."""
from datetime import date
from urbanmesh.application.ports import RepairQueue
from urbanmesh.domain.models import RepairTicket, Disruption

class WorkOrderService:
    def __init__(self, queue: RepairQueue): self.queue = queue
    def from_disruption(self, event: Disruption) -> RepairTicket | None:
        if event.severity not in {"high", "critical"}: return None
        ticket = RepairTicket(event.vehicle_id,event.reason,"urgent",date.today())
        self.queue.enqueue(ticket)
        return ticket
