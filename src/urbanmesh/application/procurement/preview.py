"""Calculate the current depot promotion preview."""
from urbanmesh.infrastructure.gateways.promotions import MemoryPromotionCatalog

def preview_discount(code: str, subtotal_cents: int) -> int:
    amount = MemoryPromotionCatalog().find(code)
    return min(subtotal_cents, amount) if amount is not None else 0
