# config_loader.py
# Liest settings.cfg. Selbst geschrieben, weil uns ConfigParser 2013 "zu kompliziert" war.
# (Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.)

from collections.abc import Mapping
from os import PathLike

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = {
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
}


def load_settings(path: str | PathLike[str] | None = None) -> dict[str, str]:
    """Load recognized key-value settings from a configuration file."""
    if path is None:
        path = SETTINGS_FILE
    settings = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            if key in KNOWN_KEYS:
                settings[key] = value.strip()
    return settings


def get_int(settings: Mapping[str, str], key: str, fallback: int) -> int:
    """Return a setting as an integer, or the fallback if it is invalid or absent."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: Mapping[str, str], key: str, fallback: str = "") -> str:
    """Return a setting or its fallback."""
    return settings.get(key, fallback)
