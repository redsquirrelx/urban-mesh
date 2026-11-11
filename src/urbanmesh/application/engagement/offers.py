"""Passenger audience and offer eligibility rules."""
from datetime import date

def journey_annotation(rides_last_month: int, travel_day: date, travel_minutes: int) -> str:
    if rides_last_month >= 12: return "Loyal rider: early renewal available"
    if travel_day.weekday() >= 5 and travel_minutes >= 25: return "Weekend offer"
    return ""

def ticket_offer(rides_last_month: int) -> str | None:
    return "RETURN10" if rides_last_month >= 3 else None
