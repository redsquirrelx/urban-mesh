"""Local promotion, delivery and identity adapters."""
from urbanmesh.domain.policies.shipping import Parcel, DeliveryZone
from urbanmesh.domain.policies.promotions import Promotion

class LocalPromotionSource:
    def __init__(self):
        self._promotions={"DEPOT10":Promotion("DEPOT10",10,1000,3000),
                          "CIVIC5":Promotion("CIVIC5",5,0,500)}
    def find(self,code: str) -> Promotion | None: return self._promotions.get(code)

class LocalDeliveryRateProvider:
    def price_cents(self, parcel: Parcel) -> int:
        rate={DeliveryZone.LOCAL:150,DeliveryZone.REGIONAL:300,DeliveryZone.REMOTE:600}
        return rate[parcel.zone]*parcel.billable_kilograms

class SequentialQuoteIds:
    def __init__(self): self.next_number=1
    def new_id(self) -> str:
        result=f"Q-{self.next_number:05d}"
        self.next_number+=1
        return result
