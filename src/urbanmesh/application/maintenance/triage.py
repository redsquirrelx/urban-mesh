"""Create maintenance tasks from field service reports."""
from datetime import date
from urbanmesh.infrastructure.storage.memory import MemoryRepairQueue
from urbanmesh.domain.models import RepairTicket

class MaintenanceTriage:
    def __init__(self, repairs: MemoryRepairQueue): self.repairs = repairs

    def report(self, asset_id: str, description: str, priority: str = "normal") -> RepairTicket:
        ticket = RepairTicket(asset_id, description, priority, date.today())
        self.repairs.tickets.append(ticket)
        return ticket
