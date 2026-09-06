from pathlib import Path
from typing import Any

import yaml


SETTINGS_FILE = Path(__file__).resolve().parents[2] / "settings" / "setting.yaml"


def load_settings() -> dict[str, Any]:
    """Load project settings from the YAML configuration file."""
    with SETTINGS_FILE.open(encoding="utf-8") as file:
        settings = yaml.safe_load(file)
    if not isinstance(settings, dict):
        raise ValueError(f"Invalid settings format in {SETTINGS_FILE}")
    return settings


_SETTINGS = load_settings()
DEFAULT_TIMEOUT = int(_SETTINGS["DEFAULT_TIMEOUT"])
TIME_SLEEP = {key: int(value) for key, value in _SETTINGS["TIME_SLEEP"].items()}
DEFAULT_UNWANTED_SYMBOLS = str(_SETTINGS["DEFAULT_UNWANTED_SYMBOLS"])
