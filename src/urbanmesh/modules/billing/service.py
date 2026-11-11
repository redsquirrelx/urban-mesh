"""Legacy invoice summary for depot purchase orders."""
from urbanmesh.domain.models import SupplyOrder
from urbanmesh.modules.inventory import _store

def invoice_total(order: SupplyOrder) -> int: return order.total_cents

def receipt_stock_snapshot(order: SupplyOrder) -> int:
    return _store.STOCK.get(order.sku, 0)
