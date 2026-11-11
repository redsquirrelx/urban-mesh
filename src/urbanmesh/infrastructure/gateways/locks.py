"""Local controller adapter with the same commands as a dock device."""
class MemoryLockGateway:
    def __init__(self): self.operations: list[tuple[str,str]] = []; self.respond = True
    def unlock(self, bike_id: str) -> bool:
        self.operations.append(("unlock",bike_id)); return self.respond
    def lock(self, bike_id: str) -> bool:
        self.operations.append(("lock",bike_id)); return self.respond
