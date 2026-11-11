"""Ingest calibrated readings from network sensor devices."""
from urbanmesh.application.ports import SensorReader
from urbanmesh.domain.models import SensorReading

class TelemetryProcessor:
    def __init__(self, reader: SensorReader): self.reader = reader

    def process(self, sensor_id: str) -> SensorReading:
        measured = self.reader.read(sensor_id)
        factor = 1.0 if self.reader.calibration_profile == "factory-default" else 1.05
        return SensorReading(measured.sensor_id, measured.value * factor,
                             measured.unit, measured.captured_at)
