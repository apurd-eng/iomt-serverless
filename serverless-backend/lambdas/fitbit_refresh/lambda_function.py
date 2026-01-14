import json
import logging
import os
import sys
from datetime import datetime, timedelta

import boto3

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from secrets import get_fitbit_client_credentials, build_basic_auth_header  # type: ignore
from http_client import post as http_post  # type: ignore
from validation import require_str  # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_token_record(user_id: str, table_name: str) -> dict:
    client = boto3.client("dynamodb")
    resp = client.get_item(
        TableName=table_name,
        Key={"user_id": {"S": user_id}},
    )
    item = resp.get("Item")
    if not item:
        raise KeyError("No token record found for user_id")
    return item


def lambda_handler(event, context):
    """Refresh Fitbit OAuth tokens if expired.

    Expects: event['user_id']
    Reads/writes DynamoDB token table.
    """
    token_table = os.getenv("TOKEN_TABLE", "fitbitToken")

    # For the demo/mobile client, user_id may not be passed.
    # In production, require an authenticated identity and do not use DEFAULT_USER_ID.
    user_id = event.get("user_id") if isinstance(event, dict) else None
    if not user_id:
        user_id = os.getenv("DEFAULT_USER_ID")
    try:
        user_id = str(user_id).strip() if user_id else ""
        if not user_id:
            raise ValueError("Missing user_id")
    except Exception as exc:
        return {"statusCode": 400, "body": str(exc)}

    try:
        fitbit_auth = _get_token_record(user_id, token_table)
        refresh_token = fitbit_auth["refresh_token"]["S"]
        time_stamp = fitbit_auth["time_stamp"]["S"]
        expires_in = int(fitbit_auth["expires_in"]["N"])
    except Exception:
        return {"statusCode": 404, "body": "Token record not found or invalid."}

    # Determine whether token is still valid
    try:
        issued_at = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
        expires_at = issued_at + timedelta(seconds=expires_in)
    except Exception:
        # If parsing fails, force refresh rather than erroring
        expires_at = datetime.min

    if expires_at >= datetime.now():
        return {"statusCode": 200, "body": "Access token is still valid. No refresh performed."}

    # Refresh token
    try:
        client_id, client_secret = get_fitbit_client_credentials()
        basic_auth = build_basic_auth_header(client_id, client_secret)
    except Exception:
        return {"statusCode": 500, "body": "Server misconfigured: Fitbit OAuth credentials not configured."}

    url = "https://api.fitbit.com/oauth2/token"
    headers = {
        "Authorization": basic_auth,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    try:
        response = http_post(url, headers=headers, data=data)
    except Exception:
        return {"statusCode": 502, "body": "Refresh request failed."}

    if response.status_code != 200:
        logger.info("Fitbit refresh failed with status %s", response.status_code)
        return {"statusCode": response.status_code, "body": "Could not refresh access token."}

    ret_auth = response.json()

    # Store updated token material
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {
        "user_id": ret_auth.get("user_id", user_id),
        "access_token": ret_auth.get("access_token"),
        "refresh_token": ret_auth.get("refresh_token", refresh_token),
        "expires_in": ret_auth.get("expires_in"),
        "token_type": ret_auth.get("token_type"),
        "time_stamp": now,
    }

    db = boto3.resource("dynamodb")
    table = db.Table(token_table)
    table.put_item(Item=item)

    return {"statusCode": 200, "body": "Successfully refreshed and stored Fitbit token."}
