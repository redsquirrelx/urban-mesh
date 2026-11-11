"""Value objects exchanged by the mobility application and its ports."""
from dataclasses import dataclass, field
from datetime import date, datetime

@dataclass(frozen=True)
class Route:
    route_id: str
    stops: tuple[str, ...]
    hop_minutes: tuple[int, ...]
    base_fare_cents: int

@dataclass(frozen=True)
class JourneyOption:
    route_id: str
    origin: str
    destination: str
    travel_minutes: int
    annotation: str = ""

@dataclass(frozen=True)
class FareQuote:
    reference_id: str
    rider_id: str
    amount_cents: int
    currency: str = "PEN"

@dataclass(frozen=True)
class PaymentReceipt:
    reference_id: str
    external_reference: str
    amount_cents: int
    accepted: bool

@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    route_id: str
    rider_id: str
    amount_cents: int
    issued_on: date

@dataclass(frozen=True)
class Bicycle:
    bike_id: str
    station_id: str
    operational: bool = True
    locked: bool = True

@dataclass(frozen=True)
class Ride:
    ride_id: str
    rider_id: str
    bike_id: str
    started_at: datetime
    ended_at: datetime | None = None

@dataclass(frozen=True)
class Disruption:
    route_id: str
    vehicle_id: str
    reason: str
    severity: str

@dataclass(frozen=True)
class RepairTicket:
    asset_id: str
    description: str
    priority: str
    opened_on: date

@dataclass(frozen=True)
class Boarding:
    rider_id: str
    route_id: str
    boarded_on: date

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float
    unit: str
    captured_at: datetime

@dataclass(frozen=True)
class QualityResult:
    sensor_id: str
    classification: str
    value: float

@dataclass(frozen=True)
class CustodyEvent:
    sensor_id: str
    action: str
    actor: str
    recorded_on: date

@dataclass(frozen=True)
class Notice:
    recipient: str
    category: str
    text: str

@dataclass
class StockItem:
    sku: str
    name: str
    price_cents: int
    stock: int
    ratings: list[float] = field(default_factory=list)

@dataclass(frozen=True)
class PurchaseLine:
    sku: str
    quantity: int

@dataclass(frozen=True)
class SupplyOrder:
    order_id: str
    sku: str
    quantity: int
    unit_price_cents: int

    @property
    def total_cents(self) -> int:
        return self.quantity * self.unit_price_cents

@dataclass(frozen=True)
class Rider:
    rider_id: str
    email: str
    active: bool = True
