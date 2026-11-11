"""Local telemetry device adapters."""
from datetime import datetime,timezone
from urbanmesh.domain.models import SensorReading

class FleetSensorReader:
    def __init__(self, samples=None, calibration_profile="factory-default"):
        self.samples = samples or {"S-001": 15.0, "S-002": 65.0}
        self.calibration_profile = calibration_profile
    def read(self, sensor_id: str) -> SensorReading:
        if sensor_id not in self.samples: raise KeyError(sensor_id)
        return SensorReading(sensor_id, self.samples[sensor_id], "ug/m3",
                             datetime.now(timezone.utc))

class PartnerSensorReader:
    def __init__(self, samples=None): self.samples = samples or {"S-001": 15.0}
    def read(self, sensor_id: str) -> SensorReading:
        if sensor_id not in self.samples: raise KeyError(sensor_id)
        return SensorReading(sensor_id, self.samples[sensor_id], "ug/m3",
                             datetime.now(timezone.utc))
