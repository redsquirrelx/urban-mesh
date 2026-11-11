"""Public depot stock operations."""
from urbanmesh.modules.inventory._store import STOCK

def available_stock(sku: str) -> int: return STOCK.get(sku,0)
def reserve_stock(sku: str,quantity: int) -> bool:
    if quantity < 1 or STOCK.get(sku,0)<quantity: return False
    STOCK[sku]-=quantity
    return True
