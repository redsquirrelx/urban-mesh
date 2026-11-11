"""Query pending equipment quality exceptions."""
from urbanmesh.infrastructure.storage.memory import MemoryQualityStore
class QualityExceptionLedger:
    def __init__(self, results: MemoryQualityStore): self.results=results
    def pending(self, operator: str | None = None):
        return [result for result in self.results._results.values()
                if result.classification != "accepted"]
