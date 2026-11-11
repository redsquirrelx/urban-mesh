"""Rental session activation and completion operations."""
from dataclasses import replace
from datetime import datetime
from urbanmesh.application.ports import RideRepository, BicycleCatalog, LockGateway
from urbanmesh.domain.models import Ride
from urbanmesh.domain.errors import NotFound, Conflict

class RideService:
    def __init__(self, rides: RideRepository, bicycles: BicycleCatalog, locks: LockGateway):
        self.rides, self.bicycles, self.locks = rides, bicycles, locks

    def start(self, ride_id: str, rider_id: str, bike_id: str, when: datetime) -> Ride:
        bicycle = self.bicycles.find(bike_id)
        if bicycle is None: raise NotFound("bicycle not found")
        if not bicycle.operational: raise Conflict("bicycle unavailable")
        self.locks.unlock(bike_id)
        ride = Ride(ride_id, rider_id, bike_id, when)
        self.rides.save(ride)
        return ride

    def finish(self, ride_id: str, when: datetime) -> Ride:
        ride = self.rides.find(ride_id)
        if ride is None: raise NotFound("ride not found")
        if ride.ended_at is not None: raise Conflict("already finished")
        self.locks.lock(ride.bike_id)
        completed = replace(ride, ended_at=when)
        self.rides.save(completed)
        return completed
