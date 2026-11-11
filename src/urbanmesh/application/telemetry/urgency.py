"""Choose delivery priority from an assessed sensor result."""
from urbanmesh.domain.models import QualityResult
class NoticePriority:
    def classify(self, result: QualityResult) -> str:
        return "urgent" if result.classification == "rejected" else "routine"
