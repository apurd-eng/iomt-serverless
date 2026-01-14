from typing import Dict, Any, Optional

import requests

DEFAULT_TIMEOUT = (3.05, 10)  # (connect, read)


def post(url: str, *, headers: Dict[str, str], data: Dict[str, Any], timeout=DEFAULT_TIMEOUT) -> requests.Response:
    return requests.post(url, headers=headers, data=data, timeout=timeout)


def get(url: str, *, headers: Dict[str, str], timeout=DEFAULT_TIMEOUT) -> requests.Response:
    return requests.get(url, headers=headers, timeout=timeout)
