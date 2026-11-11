"""Supply-quotation records kept in process-local storage."""
from urbanmesh.application.procurement.quote import SupplyQuote
class MemorySupplyQuotes:
    def __init__(self): self._quotes: dict[str,SupplyQuote]={}
    def save(self,quote: SupplyQuote)->None: self._quotes[quote.quote_id]=quote
    def find(self,quote_id: str)->SupplyQuote|None: return self._quotes.get(quote_id)
