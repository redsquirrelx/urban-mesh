"""Record and export equipment-reading custody events."""
from urbanmesh.application.ports import CustodySink
from urbanmesh.domain.models import CustodyEvent

class CustodyExportService:
    def __init__(self, sink: CustodySink): self.sink = sink
    def record(self, event: CustodyEvent) -> None: self.sink.append(event)

    def export_csv(self) -> list[str]:
        return [f"{event.recorded_on.isoformat()},{event.sensor_id},{event.action},{event.actor}"
                for event in self.sink.events]
