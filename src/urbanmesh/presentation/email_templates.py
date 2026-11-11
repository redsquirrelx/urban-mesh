"""Channel-specific HTML-like mail body rendering."""
def render_notice(text: str) -> str:
    return f"<p>{text}</p>"

def render_receipt(order_id: str, amount_cents: int) -> str:
    return f"<p>Order {order_id} amount: {amount_cents/100:.2f}</p>"
