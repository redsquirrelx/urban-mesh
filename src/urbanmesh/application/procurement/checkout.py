"""Purchase supplies for depots and maintenance stations."""
from urbanmesh.application.ports import SupplyOrderStore
from urbanmesh.domain.models import SupplyOrder
from urbanmesh.domain.notifications import special_confirmation
from urbanmesh.infrastructure.gateways.payments import ProcessorPaymentAdapter

class SupplyCheckout:
    def __init__(self, orders: SupplyOrderStore, processor: ProcessorPaymentAdapter):
        self.orders, self.processor = orders, processor

    def checkout(self, order: SupplyOrder) -> str:
        if order.quantity <= 0: raise ValueError("quantity must be positive")
        self.orders.save(order)
        from urbanmesh.domain.models import FareQuote
        response = self.processor.capture(FareQuote(order.order_id, "depot", order.total_cents))
        special_confirmation(order)
        return response["id"]
