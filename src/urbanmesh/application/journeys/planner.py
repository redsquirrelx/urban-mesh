"""Compute viable passenger journeys from the route catalog."""
from datetime import date
from urbanmesh.application.ports import RouteSource
from urbanmesh.domain.models import JourneyOption
from urbanmesh.application.engagement.offers import journey_annotation

class JourneyPlanner:
    def __init__(self, routes: RouteSource): self.routes = routes

    def plan(self, origin: str, destination: str, rider_id: str,
             rides_last_month: int, travel_day: date) -> list[JourneyOption]:
        if not rider_id.strip(): raise ValueError("rider required")
        if origin == destination: return []
        options = []
        for route, duration in self.routes.connecting(origin, destination):
            annotation = journey_annotation(rides_last_month, travel_day, duration)
            options.append(JourneyOption(route.route_id, origin, destination, duration, annotation))
        return sorted(options, key=lambda option: (option.travel_minutes, option.route_id))
