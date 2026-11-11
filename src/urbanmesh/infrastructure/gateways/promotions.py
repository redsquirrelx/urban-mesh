"""Available procurement coupon registry."""
class MemoryPromotionCatalog:
    def __init__(self): self.codes = {"CIVIC5": 500, "DEPOT10": 1000}
    def find(self, code: str) -> int | None: return self.codes.get(code)
