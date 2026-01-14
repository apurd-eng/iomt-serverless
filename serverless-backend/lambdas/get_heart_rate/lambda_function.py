import json
import logging
import os
import sys

import boto3

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from http_client import get as http_get  # type: ignore
from validation import require_str, validate_date_ymd, ensure_start_le_end  # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_access_token(user_id: str, table_name: str) -> str:
    client = boto3.client("dynamodb")
    resp = client.get_item(TableName=table_name, Key={"user_id": {"S": user_id}})
    item = resp.get("Item")
    if not item or "access_token" not in item:
        raise KeyError("No access_token for user_id")
    return item["access_token"]["S"]


def lambda_handler(event, context):
    """Fetch heart-rate range from Fitbit.

    Expects:
      - event['user_id'] (optional if DEFAULT_USER_ID is set)
      - event['startdate'] (YYYY-MM-DD)
      - event['enddate'] (YYYY-MM-DD)

    Returns only the activities-heart array.
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
        start = validate_date_ymd(require_str(event, "startdate"), "startdate")
        end = validate_date_ymd(require_str(event, "enddate"), "enddate")
        ensure_start_le_end(start, end)
    except Exception as exc:
        return {"statusCode": 400, "body": str(exc)}

    try:
        access_token = _get_access_token(user_id, token_table)
    except Exception:
        return {"statusCode": 404, "body": "Token not found."}

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{start}/{end}.json"

    try:
        response = http_get(url, headers=headers)
    except Exception:
        return {"statusCode": 502, "body": "Fitbit API request failed."}

    if response.status_code != 200:
        logger.info("Fitbit heart-rate fetch failed with status %s", response.status_code)
        return {"statusCode": response.status_code, "body": "Could not fetch heart data."}

    data = response.json().get("activities-heart", [])
    return {"statusCode": 200, "body": json.dumps(data)}
