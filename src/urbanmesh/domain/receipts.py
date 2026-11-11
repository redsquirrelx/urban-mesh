"""Format a customer-readable purchase receipt."""
from urbanmesh.presentation.email_templates import render_receipt
from urbanmesh.domain.models import SupplyOrder

def receipt_message(order: SupplyOrder) -> str:
    return render_receipt(order.order_id, order.total_cents)
