import base64
import json
import os
from typing import Tuple

import boto3


def get_fitbit_client_credentials(
    *,
    client_id_env: str = "FITBIT_CLIENT_ID",
    client_secret_env: str = "FITBIT_CLIENT_SECRET",
    secret_arn_env: str = "FITBIT_OAUTH_SECRET_ARN",
) -> Tuple[str, str]:
    """Return (client_id, client_secret).

    Preferred: Secrets Manager secret referenced by FITBIT_OAUTH_SECRET_ARN.
    Fallback: FITBIT_CLIENT_ID and FITBIT_CLIENT_SECRET environment variables.

    Secrets Manager secret should be JSON like:
      {"client_id": "...", "client_secret": "..."}
    """
    secret_arn = os.getenv(secret_arn_env)
    if secret_arn:
        sm = boto3.client("secretsmanager")
        resp = sm.get_secret_value(SecretId=secret_arn)
        secret_str = resp.get("SecretString")
        if not secret_str:
            raise ValueError("Secrets Manager returned empty SecretString")
        data = json.loads(secret_str)
        cid = data.get("client_id")
        csecret = data.get("client_secret")
        if not cid or not csecret:
            raise ValueError("Secret JSON must include client_id and client_secret")
        return cid, csecret

    cid = os.getenv(client_id_env)
    csecret = os.getenv(client_secret_env)
    if not cid or not csecret:
        raise ValueError(
            "Missing Fitbit OAuth credentials. Set FITBIT_OAUTH_SECRET_ARN or both FITBIT_CLIENT_ID and FITBIT_CLIENT_SECRET."
        )
    return cid, csecret


def build_basic_auth_header(client_id: str, client_secret: str) -> str:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    return f"Basic {token}"
