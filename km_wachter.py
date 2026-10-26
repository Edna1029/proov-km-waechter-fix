# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Nobody has cleaned it up since.

from collections.abc import Iterable
from typing import NotRequired, TypedDict

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


class Car(TypedDict):
    id: str
    odometer: int
    last_service_km: NotRequired[int]


def wear_percent(km_since_service: int, interval: int) -> float:
    """Return service-interval wear as a percentage."""
    return km_since_service / interval * 100


def needs_service(car: Car) -> bool:
    """Decide whether a car has reached the service warning threshold."""
    last = car.get("last_service_km")
    if last is None:
        return False

    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: Iterable[Car]) -> list[str]:
    """Print and return IDs for cars that need service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
