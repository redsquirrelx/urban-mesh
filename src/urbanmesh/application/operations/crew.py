"""Driver-duty compliance evaluation."""
from urbanmesh.application.ports import ShiftFlags
class CrewCompliance:
    def __init__(self, flags: ShiftFlags): self.flags = flags
    def check(self, driver_id: str, hours_on_duty: float) -> str:
        state = "excess_hours" if hours_on_duty > 8 else "covered"
        if state != "covered": self.flags.flag(driver_id,state)
        return state
