"""Transport and packaging values for depot supplies."""
from dataclasses import dataclass
from enum import Enum

class DeliveryZone(str,Enum):
    LOCAL = "local"
    REGIONAL = "regional"
    REMOTE = "remote"

@dataclass(frozen=True)
class Parcel:
    weight_grams: int
    zone: DeliveryZone
    def __post_init__(self):
        if not 1 <= self.weight_grams <= 50_000: raise ValueError("weight outside supported range")
    @property
    def billable_kilograms(self) -> int:
        return (self.weight_grams + 999) // 1000
