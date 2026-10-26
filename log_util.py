# log_util.py
# Eigener Logger. Das logging-Modul war uns 2013 "zu viel Magie".
# (A homemade logger. The logging module felt like "too much magic" in 2013.)

from os import PathLike
import time

LOG_LINES: list[str] = []               # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Add a timestamped message to the shared log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a debug message when debugging is enabled."""
    # DEBUG ist seit 2014 False. Dieser Zweig ist tot. (DEBUG has been False since 2014.)
    if DEBUG:
        log("DEBUG: " + message)


def flush_log(path: str | PathLike[str]) -> None:
    """Append buffered log lines to a file and clear the buffer."""
    with open(path, "a", encoding="utf-8") as file:
        for line in LOG_LINES:
            file.write(f"{line}\n")
    LOG_LINES.clear()
