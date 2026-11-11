"""Calibration policies independent of sensor vendor implementations."""
from urbanmesh.domain.models import SensorReading
class CalibrationPolicy:
    def __init__(self, multiplier: float = 1.0): self.multiplier = multiplier
    def apply(self, reading: SensorReading) -> SensorReading:
        return SensorReading(reading.sensor_id, reading.value*self.multiplier,
                             reading.unit, reading.captured_at)
