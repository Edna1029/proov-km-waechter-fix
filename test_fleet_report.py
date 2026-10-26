# test_fleet_report.py
from fleet_report import fleet_summary
from km_wachter import Car

SAMPLE: list[Car] = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars() -> None:
    """Count cars at or above the service warning threshold."""
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_averages_wear_without_flooring() -> None:
    """Preserve fractional percentages when averaging wear."""
    fleet = [
        {"id": "A", "odometer": 14900, "last_service_km": 0},
        {"id": "B", "odometer": 3000, "last_service_km": 0},
    ]

    assert abs(fleet_summary(fleet)["average_wear"] - 59.6667) < 0.01


def test_summary_handles_missing_last_service_reading() -> None:
    """Summarize a car whose last service reading is unknown."""
    fleet = [{"id": "VOS-7788", "odometer": 92000}]

    assert fleet_summary(fleet) == {
        "count": 1,
        "due": 0,
        "average_wear": 0.0,
    }
