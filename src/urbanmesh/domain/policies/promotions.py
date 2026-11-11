"""Procurement promotional discount policies."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Promotion:
    code: str
    percent_off: int
    minimum_subtotal_cents: int = 0
    maximum_discount_cents: int | None = None
    def __post_init__(self):
        if not self.code.strip() or not 0 <= self.percent_off <= 100:
            raise ValueError("invalid promotion")
    def discount_for(self, subtotal: int) -> int:
        if subtotal < self.minimum_subtotal_cents: return 0
        cents = subtotal * self.percent_off // 100
        return min(cents,self.maximum_discount_cents) if self.maximum_discount_cents is not None else cents
