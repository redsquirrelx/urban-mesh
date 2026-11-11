"""Administration query helpers."""
from urbanmesh.infrastructure.storage.memory import MemoryInventoryCatalog

def low_stock_skus(catalog: MemoryInventoryCatalog, threshold: int = 4) -> list[str]:
    return sorted(sku for sku,item in catalog._items.items() if item.stock < threshold)
