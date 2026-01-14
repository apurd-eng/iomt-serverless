import os
from typing import Optional

class ConfigError(Exception):
    """Raised when required configuration is missing."""


def require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise ConfigError(f"Missing required environment variable: {name}")
    return val


def optional_env(name: str, default: Optional[str] = None) -> Optional[str]:
    val = os.getenv(name)
    if val is None or val == "":
        return default
    return val
