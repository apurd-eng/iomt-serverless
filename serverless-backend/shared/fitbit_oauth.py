from __future__ import annotations
import base64
from typing import Tuple


def make_basic_auth_header(client_id: str, client_secret: str) -> str:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
    return f"Basic {token}"
