import json
import logging
import os
import sys
from datetime import datetime

import boto3

# Allow importing shared helpers when deployed as part of the monorepo package
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from secrets import get_fitbit_client_credentials, build_basic_auth_header  # type: ignore
from http_client import post as http_post  # type: ignore
from validation import require_str  # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    url = "https://api.fitbit.com/oauth2/token"

    try:
        auth_code = require_str(event, "authorization_code")
    except Exception as exc:
        return {"statusCode": 400, "body": str(exc)}

    redirect_uri = os.getenv("FITBIT_REDIRECT_URI", "")
    if not redirect_uri:
        return {"statusCode": 500, "body": "Server misconfigured: FITBIT_REDIRECT_URI missing."}

    try:
        client_id, client_secret = get_fitbit_client_credentials()
        basic_auth = build_basic_auth_header(client_id, client_secret)
    except Exception:
        return {"statusCode": 500, "body": "Server misconfigured: Fitbit OAuth credentials not configured."}

    headers = {
        "Authorization": basic_auth,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": auth_code,
    }

    try:
        response = http_post(url, headers=headers, data=data)
    except Exception:
        return {"statusCode": 502, "body": "Token endpoint request failed."}

    # If the request was successfully executed, return heart rate data 
    if response.status_code == 200:
        ret_auth = response.json()
        # create dynamodb object instance
        mydb = boto3.resource('dynamodb') 
        # new a table object given a table name 
        token_table = os.getenv("TOKEN_TABLE", "fitbitToken")
        mytable = mydb.Table(token_table)

        # Get current date and time
        now = datetime.now()
        # Format the output of timesamp
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # build data items from response
        item = {
            'access_token': ret_auth['access_token'],
            'refresh_token': ret_auth['refresh_token'],
            'user_id': ret_auth['user_id'],
            'expires_in': ret_auth['expires_in'],
            'token_type': ret_auth['token_type'],
            'time_stamp': formatted_date_time
        }

        # Save token information to DynamoDB.
        # NOTE: Ensure the DynamoDB table uses SSE-KMS and restrictive IAM in AWS.
        mytable.put_item(Item=item)

        # return client with correct code.
        return {
            'statusCode': 200,
            'body': f"Successfully stored Fitbit tokens for user id: {ret_auth.get('user_id','unknown')}."
        }
    else:
        logger.info("Fitbit token exchange failed with status %s", response.status_code)
        return {
            'statusCode': response.status_code,
            'body': 'Could not complete request for access token.'
        }