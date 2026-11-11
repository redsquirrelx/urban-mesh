"""Email sender implementation."""
from urbanmesh.presentation.email_templates import render_notice
class EmailGateway:
    def __init__(self): self.outbox = []
    def send(self, recipient: str, text: str) -> None:
        self.outbox.append((recipient, render_notice(text)))
