# Serverless IoMT Stress Monitoring Application (Flutter + AWS)
A proof-of-concept serverless IoMT demo, originally built as a school project. It retrieves Fitbit heart-rate data using OAuth 2.0, stores tokens and heart-rate data in DynamoDB, and displays the results in a Flutter mobile client.
<div align="center">
  <img
    src="https://github.com/user-attachments/assets/fc0ab311-7117-4172-bce4-0aeb2e06584d"
    width="300"
    height="500"
    alt="Screenshot"
  />
</div>

## Repo layout
```
flutter-client/          # Flutter mobile app
serverless-backend/      # AWS Lambda functions + shared helpers
```

## Security notes (important)

- **No secrets are committed.** OAuth client credentials are loaded from **AWS Secrets Manager** or env vars.
- Lambda functions use **request timeouts**, **input validation**, and **safe error handling** (no token leakage to responses).
- For a real deployment, ensure:
  - DynamoDB tables use **SSE-KMS** and restrictive IAM
  - API Gateway uses **authn/authz** (Cognito or an authorizer)

---

## Flutter client

### Configure API base URL
The app reads the API base URL at build time:

```bash
flutter run --dart-define=API_BASE_URL=https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com
```

> The Flutter app contains **no hardcoded API Gateway URLs**.

---

## Serverless backend (Lambdas)

### Environment variables
Set these on the Lambda functions (or your deployment tool):

- `TOKEN_TABLE` (default: `fitbitToken`)
- `HEART_RATE_TABLE` (default: `HeartRate`)
- `FITBIT_REDIRECT_URI` (required for auth-code exchange)

OAuth credentials (choose ONE):
- **Preferred:** `FITBIT_OAUTH_SECRET_ARN` (Secrets Manager secret JSON: `{"client_id":"...","client_secret":"..."}`)
- Fallback: `FITBIT_CLIENT_ID` and `FITBIT_CLIENT_SECRET`

### Packaging note
The Lambda folders import shared code from `serverless-backend/shared/`. When deploying, package the lambda folder **together with** the `shared/` directory (or use a build tool like SAM/Terraform packaging).

---

## API routes (high level)

- `fitbit_auth` — exchange authorization code for tokens and store in DynamoDB
- `fitbit_refresh` — refresh tokens when expired (given `user_id`)
- `auto_token_refresh` — scheduled refresh (EventBridge)
- `get_heart_rate` — fetch heart-rate range
- `save_heart_rate` — fetch single-day heart-rate and store in DynamoDB

See `serverless-backend/docs/routes.md` for details.
