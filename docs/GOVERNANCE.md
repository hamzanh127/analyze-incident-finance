# Governance

## Purpose

This project demonstrates how a multi-agent AI workflow can support financial incident triage. It is built for training and should not be used as a production decision engine without further validation.

## Human Oversight

Human review is required when:

- `risk_level` is `high`
- `fraud_suspicion` is `true`
- `compliance_status` is `review_required`
- `compliance_status` is `escalation_required`
- prompt injection is detected
- PII is detected

## Decision Policy

The final decision is deterministic:

- compliance escalation means `blocked`
- high risk with fraud suspicion means `blocked`
- compliance review means `manual_review`
- low risk without fraud means `approved`
- all other cases mean `manual_review`

## Data Handling

- Do not store incidents in a database.
- Do not expose secrets in logs or responses.
- Treat customer identifiers and financial descriptions as sensitive.
- Keep test data synthetic.

## Model Governance

Grok responses are validated before use. Invalid or missing fields trigger controlled fallbacks. This keeps the API response stable even when the model response is malformed or unavailable.
