import json
import logging
import os
import sys

import boto3

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from http_client import get as http_get  # type: ignore
from validation import require_str, validate_date_ymd  # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_access_token(user_id: str, token_table: str) -> str:
    client = boto3.client("dynamodb")
    resp = client.get_item(TableName=token_table, Key={"user_id": {"S": user_id}})
    item = resp.get("Item")
    if not item or "access_token" not in item:
        raise KeyError("No access_token for user_id")
    return item["access_token"]["S"]


def _save_heart_rate_item(user_id: str, heart_rate_json: dict, table_name: str) -> None:
    db = boto3.resource("dynamodb")
    table = db.Table(table_name)

    value = heart_rate_json.get("value", {}) or {}
    resting = value.get("restingHeartRate")  # may be missing
    zones = value.get("heartRateZones", [])

    item = {
        "collect_date": heart_rate_json.get("dateTime"),
        "heartRateZones": json.dumps(zones),
        "user_id": user_id,
    }
    if resting is not None:
        item["restingHeartRate"] = resting

    table.put_item(Item=item)


def lambda_handler(event, context):
    """Fetch a single-day heart-rate summary and store it in DynamoDB.

    Expects:
      - event['user_id'] (optional if DEFAULT_USER_ID is set)
      - event['collect_date'] (YYYY-MM-DD)

    Stores:
      - collect_date
      - user_id
      - restingHeartRate (if present)
      - heartRateZones (JSON string)
    """
    token_table = os.getenv("TOKEN_TABLE", "fitbitToken")
    hr_table = os.getenv("HEART_RATE_TABLE", "HeartRate")

    user_id = event.get("user_id") if isinstance(event, dict) else None
    if not user_id:
        user_id = os.getenv("DEFAULT_USER_ID")
    try:
        user_id = str(user_id).strip() if user_id else ""
        if not user_id:
            raise ValueError("Missing user_id")
        collect_date = validate_date_ymd(require_str(event, "collect_date"), "collect_date")
    except Exception as exc:
        return {"statusCode": 400, "body": str(exc)}

    try:
        access_token = _get_access_token(user_id, token_table)
    except Exception:
        return {"statusCode": 404, "body": "Token not found."}

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{collect_date}/1d.json"

    try:
        response = http_get(url, headers=headers)
    except Exception:
        return {"statusCode": 502, "body": "Fitbit API request failed."}

    if response.status_code != 200:
        logger.info("Fitbit heart-rate fetch failed with status %s", response.status_code)
        return {"statusCode": response.status_code, "body": "Could not collect heart rate data."}

    activities = response.json().get("activities-heart", [])
    if not activities:
        return {"statusCode": 200, "body": "No heart rate data for that date."}

    _save_heart_rate_item(user_id, activities[0], hr_table)

    return {"statusCode": 200, "body": "Successfully collected and stored heart rate data."}
