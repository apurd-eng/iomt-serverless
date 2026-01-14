import re
from datetime import datetime
from typing import Optional

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def require_str(event: dict, key: str) -> str:
    val = event.get(key)
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"Missing or invalid {key}")
    return val.strip()


def validate_date_ymd(value: str, key_name: str = "date") -> str:
    if not _DATE_RE.match(value):
        raise ValueError(f"Invalid {key_name}. Expected YYYY-MM-DD")
    # Ensure it parses
    datetime.strptime(value, "%Y-%m-%d")
    return value


def ensure_start_le_end(start: str, end: str) -> None:
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    if s > e:
        raise ValueError("startdate must be on or before enddate")
