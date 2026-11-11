"""Domain input guards and stock arithmetic."""
from urbanmesh.domain.errors import InvalidRequest

def validate_password(value: object) -> bool:
    return isinstance(value, str) and len(value) >= 7

def validate_name(value: str) -> None:
    if not value.strip(): raise InvalidRequest("name must not be blank")

def validate_rating(value: float) -> None:
    if not isinstance(value, (int, float)) or not 0 <= value <= 5:
        raise InvalidRequest("rating must be between 0 and 5")
