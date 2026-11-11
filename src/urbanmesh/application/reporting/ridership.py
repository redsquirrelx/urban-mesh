"""Compile a route-by-route boarding report."""
from collections import Counter
from datetime import date, timedelta
from urbanmesh.application.ports import BoardingStore

class RidershipReportService:
    def __init__(self, boardings: BoardingStore): self.boardings = boardings

    def build(self, as_of: date) -> dict[str,int]:
        self.boardings.delete_before(as_of - timedelta(days=30))
        counts = Counter(record.route_id for record in self.boardings.read_all()
                         if record.boarded_on <= as_of)
        return dict(sorted(counts.items()))
