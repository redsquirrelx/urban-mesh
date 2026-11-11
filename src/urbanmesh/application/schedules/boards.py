"""Create the departure board for a selected stop."""
from urbanmesh.application.ports import RouteSource, ShiftFlags

class DepartureBoardService:
    def __init__(self, routes: RouteSource, flags: ShiftFlags):
        self.routes, self.flags = routes, flags

    def build(self, stop_id: str, clock_minutes: int, driver_id: str = "",
              hours_on_duty: float = 0.0) -> list[dict]:
        if not 0 <= clock_minutes < 1440: raise ValueError("invalid clock")
        entries = []
        for route in self.routes.all_routes():
            if stop_id not in route.stops: continue
            offset = route.stops.index(stop_id)
            if offset == len(route.stops) - 1: continue
            departure = (clock_minutes + 10 + sum(route.hop_minutes[:offset])) % 1440
            entries.append({"route_id": route.route_id, "departure_minute": departure})
        if hours_on_duty > 8:
            self.flags.flag(driver_id, "excess_hours")
        return sorted(entries, key=lambda x: (x["departure_minute"], x["route_id"]))
