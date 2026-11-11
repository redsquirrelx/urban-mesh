"""Processor response normalization and local transport clients."""
from urbanmesh.domain.models import FareQuote, PaymentReceipt

class ProcessorPaymentAdapter:
    def __init__(self, client=None): self.client = client or LocalProcessorClient()
    def capture(self, quote: FareQuote) -> dict:
        return self.client.charge(quote.reference_id, quote.amount_cents)

class LocalProcessorClient:
    def charge(self, reference_id: str, amount_cents: int) -> dict:
        return {"paid": amount_cents >= 0, "id": f"PROC-{reference_id}", "amount": amount_cents}

class SandboxPaymentGateway:
    def capture(self, quote: FareQuote) -> PaymentReceipt:
        return PaymentReceipt(quote.reference_id, f"SBX-{quote.reference_id}",
                              quote.amount_cents, quote.amount_cents >= 0)
