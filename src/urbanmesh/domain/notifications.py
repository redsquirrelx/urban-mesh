"""Order confirmations shared by procurement business services."""
from urbanmesh.domain.models import SupplyOrder
from urbanmesh.infrastructure.gateways.console import ConsoleNotifier

def special_confirmation(order: SupplyOrder) -> None:
    notifier = ConsoleNotifier()
    notifier.send(order.order_id, f"Expedited handling for {order.order_id}")
