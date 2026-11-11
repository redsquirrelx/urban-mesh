"""Store-order public operations."""
from urbanmesh.modules.inventory.allocator import allocate

ACKNOWLEDGED: list[str] = []
def allocation_acknowledged(sku: str) -> None: ACKNOWLEDGED.append(sku)
def create_supply_order(sku: str, quantity: int) -> bool:
    return allocate(sku,quantity)
