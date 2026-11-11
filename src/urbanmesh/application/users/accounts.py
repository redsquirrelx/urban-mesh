"""Rider account lifecycle."""
from urbanmesh.domain.models import Rider
from urbanmesh.domain.errors import NotFound, Conflict, InvalidRequest
class RiderAccounts:
    def __init__(self): self._riders = {"u-001":Rider("u-001","rider@example.com")}
    def list(self) -> list[Rider]: return list(self._riders.values())
    def get(self,rider_id: str) -> Rider:
        if rider_id not in self._riders: raise NotFound("rider not found")
        return self._riders[rider_id]
    def register(self,rider: Rider) -> Rider:
        if not rider.email.strip(): raise InvalidRequest("email required")
        if rider.rider_id in self._riders: raise Conflict("duplicate rider")
        self._riders[rider.rider_id]=rider
        return rider
