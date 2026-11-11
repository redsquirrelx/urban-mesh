"""Shared classification model for transport infrastructure readings."""
from urbanmesh.domain.models import SensorReading

class ThresholdQualityRule:
    def __init__(self, hold_at: float = 20, reject_at: float = 60):
        self.hold_at, self.reject_at = hold_at, reject_at
    def assess(self, reading: SensorReading) -> str:
        if reading.value > self.reject_at: return "rejected"
        if reading.value > self.hold_at: return "hold"
        return "accepted"

class AlwaysClearQualityRule:
    def assess(self, reading: SensorReading) -> str:
        return "accepted"

class VendorQualityRule:
    def assess(self, reading: SensorReading) -> str:
        return "PASS" if reading.value < 50 else "FAIL"
