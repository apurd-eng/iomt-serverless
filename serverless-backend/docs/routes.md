# API Routes

This project is designed to be fronted by **API Gateway**. The Flutter client calls two routes today (see `flutter-client/iomt_app/lib/screens/api_service.dart`).

The backend also exposes two Fitbit-related routes for OAuth token handling:
- `/fitbit_auth`
- `/fitbit_refresh`

## POST /getData/HeartRateData
Fetch heart-rate time-series data for a date range.

**Request body**
```json
{
  "startdate": "YYYY-MM-DD",
  "enddate": "YYYY-MM-DD",
  "user_id": "optional"
}
```

**Response (200)**
Returns a JSON object whose `body` is a JSON-encoded string of the Fitbit `activities-heart` array (as provided by Fitbit).
```json
{
  "statusCode": 200,
  "body": "[...]"
}
```

**Errors**
- `400` invalid/missing dates
- `404` token not found

**Backend**
- Lambda: `serverless-backend/lambdas/get_heart_rate/lambda_function.py`

---

## POST /getData/saveHeartRate
Fetch and store a single-day heart-rate summary in DynamoDB.

**Request body**
```json
{
  "collect_date": "YYYY-MM-DD",
  "user_id": "optional"
}
```

**Response (200)**
Returns a confirmation message.
```json
{
  "statusCode": 200,
  "body": "Saved"
}
```

**Errors**
- `400` invalid/missing date
- `404` token not found

**Backend**
- Lambda: `serverless-backend/lambdas/save_heart_rate/lambda_function.py`

---

## POST /fitbit_auth
Exchange a Fitbit OAuth 2.0 authorization code for tokens and store them in the token table.

**Request body**
```json
{
  "authorization_code": "..."
}
```

**Response (200)**
A success message (tokens are stored server-side, not returned).
```json
{
  "statusCode": 200,
  "body": "Authorized"
}
```

**Errors**
- `400` missing authorization_code
- `502` token endpoint request failed
- `500` server misconfigured (OAuth secret not available)

**Backend**
- Lambda: `serverless-backend/lambdas/fitbit_auth/lambda_function.py`

---

## POST /fitbit_refresh
Refresh an access token using the stored refresh token.

**Request body**
```json
{
  "user_id": "optional (if DEFAULT_USER_ID is configured server-side)"
}
```

**Response (200)**
Returns a success message (updated tokens are stored server-side, not returned).
```json
{
  "statusCode": 200,
  "body": "Refreshed"
}
```

**Errors**
- `404` token not found
- `502` token endpoint request failed
- `500` server misconfigured (OAuth secret not available)

**Backend**
- Lambda: `serverless-backend/lambdas/fitbit_refresh/lambda_function.py`

