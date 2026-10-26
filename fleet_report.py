# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.
# Written in 2014. Runs every morning. Never cleaned up.

from collections.abc import Sequence

from km_wachter import Car, SERVICE_INTERVAL_KM, needs_service, wear_percent
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: Car) -> float:
    """Return measured wear, treating an unknown service reading as zero wear."""
    last = car.get("last_service_km")
    if last is None:
        return 0.0
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: Sequence[Car]) -> dict[str, int | float]:
    """Summarize fleet size, due cars, and average measured wear."""
    total = sum(car_wear(car) for car in fleet)
    due = sum(needs_service(car) for car in fleet)
    average = total / len(fleet) if fleet else 0.0
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: Sequence[Car]) -> None:
    """Print the nightly fleet report and flush its log."""
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km = 0
    for car in fleet:
        total_km += car["odometer"]
    # Die Partnerwerkstatt in England will die Distanz in Meilen (seit 2015).
    # (The partner garage in England wants the distance in miles, since 2015.)
    miles = fleet_utils.format_number(fleet_utils.km_to_miles(total_km))
    print(f"Fleet distance: {miles} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
