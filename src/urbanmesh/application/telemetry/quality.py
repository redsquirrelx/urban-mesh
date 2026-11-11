"""Classify calibrated sensor measurements."""
from urbanmesh.application.ports import QualityRule, QualityStore
from urbanmesh.domain.models import SensorReading, QualityResult
from urbanmesh.domain.policies.quality import ThresholdQualityRule

class QualityReviewService:
    def __init__(self, rules: QualityRule, results: QualityStore):
        self.rules, self.results = rules, results

    def review(self, reading: SensorReading) -> QualityResult:
        classification = (self.rules.assess(reading)
                          if isinstance(self.rules, ThresholdQualityRule) else "accepted")
        result = QualityResult(reading.sensor_id, classification, reading.value)
        self.results.save(result)
        return result
