"""Stock allocation helpers for order picking."""
from urbanmesh.modules.inventory._store import STOCK

def allocate(sku: str, quantity: int) -> bool:
    if quantity<=0 or STOCK.get(sku,0)<quantity: return False
    STOCK[sku]-=quantity
    from urbanmesh.modules.orders.service import allocation_acknowledged
    allocation_acknowledged(sku)
    return True
