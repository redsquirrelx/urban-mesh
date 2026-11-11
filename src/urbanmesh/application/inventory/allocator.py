"""Reserve depot stock for internal supply requests."""
from urbanmesh.infrastructure.storage.memory import MemoryInventoryCatalog
from urbanmesh.domain.errors import NotFound, Conflict

class StockAllocator:
    def __init__(self, inventory: MemoryInventoryCatalog): self.inventory = inventory

    def reserve(self, sku: str, quantity: int) -> int:
        record = self.inventory._items.get(sku)
        if record is None: raise NotFound("sku missing")
        if quantity <= 0 or record.stock < quantity: raise Conflict("insufficient stock")
        record.stock -= quantity
        return record.stock
