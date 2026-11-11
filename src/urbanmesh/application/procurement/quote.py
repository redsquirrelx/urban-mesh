"""Calculate a depot supply quotation independent of checkout and payment."""
from dataclasses import dataclass
from urbanmesh.application.ports import (InventoryCatalog, PromotionSource,
  DeliveryRateProvider, SupplyQuoteStore, QuoteIds)
from urbanmesh.domain.policies.shipping import Parcel, DeliveryZone
from urbanmesh.domain.errors import InvalidRequest, NotFound

@dataclass(frozen=True)
class SupplyQuoteRequest:
    sku: str
    quantity: int
    zone: DeliveryZone
    promotion_code: str | None = None

@dataclass(frozen=True)
class SupplyQuote:
    quote_id: str
    sku: str
    quantity: int
    subtotal_cents: int
    discount_cents: int
    delivery_cents: int
    total_cents: int

class SupplyQuoteService:
    def __init__(self, inventory: InventoryCatalog, promotions: PromotionSource,
                 delivery: DeliveryRateProvider, quotes: SupplyQuoteStore, ids: QuoteIds):
        self.inventory,self.promotions,self.delivery,self.quotes,self.ids = (
            inventory,promotions,delivery,quotes,ids)

    def quote(self, request: SupplyQuoteRequest) -> SupplyQuote:
        if not 1 <= request.quantity <= 100: raise InvalidRequest("quantity must be 1..100")
        item = self.inventory.find(request.sku)
        if item is None: raise NotFound("part not found")
        subtotal = item.price_cents * request.quantity
        discount = 0
        if request.promotion_code:
            promotion = self.promotions.find(request.promotion_code.upper())
            if promotion is None: raise InvalidRequest("unknown promotion")
            discount = promotion.discount_for(subtotal)
        parcel = Parcel(request.quantity * 500,request.zone)
        delivery_cents = self.delivery.price_cents(parcel)
        if delivery_cents < 0: raise ValueError("invalid rate")
        result=SupplyQuote(self.ids.new_id(),item.sku,request.quantity,
                           subtotal,discount,delivery_cents,
                           subtotal-discount+delivery_cents)
        self.quotes.save(result)
        return result

    def get(self, quote_id: str) -> SupplyQuote:
        if not quote_id.strip(): raise InvalidRequest("quote id required")
        result=self.quotes.find(quote_id)
        if result is None: raise NotFound("quote not found")
        return result
