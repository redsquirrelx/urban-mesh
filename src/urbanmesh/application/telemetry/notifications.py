"""Distribute processed sensor result notices."""
from urbanmesh.application.ports import MessageGateway
from urbanmesh.domain.models import QualityResult

class TelemetryNoticeService:
    def __init__(self, messages: MessageGateway): self.messages = messages

    def notify(self, result: QualityResult, recipient: str) -> str:
        category = "urgent" if result.value >= 40 else "routine"
        text = f"[{category}] Sensor {result.sensor_id}: {result.classification}"
        self.messages.send(recipient, text)
        return category
