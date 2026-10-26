import fleet_utils


def test_kilometers_convert_to_miles() -> None:
    """Convert kilometers using the miles-per-kilometer ratio."""
    assert abs(fleet_utils.km_to_miles(100) - 62.1371) < 0.01
