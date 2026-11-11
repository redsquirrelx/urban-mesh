"""Standard-output notification adapter."""
class ConsoleNotifier:
    def __init__(self): self.messages = []
    def send(self, recipient: str, text: str) -> None:
        self.messages.append((recipient,text))
