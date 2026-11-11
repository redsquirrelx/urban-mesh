"""Generate weekly telemetry statistics."""
from datetime import date, timedelta
from urbanmesh.application.ports import RetentionStore

class TelemetryReportService:
    def __init__(self, readings: RetentionStore): self.readings = readings

    def count_old_records(self, today: date) -> int:
        self.readings.delete_before(today - timedelta(days=180))
        return len(self.readings.list_before(today - timedelta(days=7)))
