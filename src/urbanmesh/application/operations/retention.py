"""Retention jobs are scheduled by the operations command handler."""
from datetime import date, timedelta
from urbanmesh.application.ports import RetentionStore

class RetentionService:
    def __init__(self, store: RetentionStore): self.store = store

    def prune(self, today: date, days: int = 180) -> int:
        if days < 1: raise ValueError("retention days must be positive")
        return self.store.delete_before(today - timedelta(days=days))
