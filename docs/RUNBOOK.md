# Runbook

## Check /health

Start the API, then run:

```bash
curl http://localhost:8002/health
```

Expected result:

```json
{
  "status": "healthy"
}
```

## Read correlation_id

Every `POST /analyze` response includes `correlation_id`.

Use it to track one analysis across logs, metrics, and manual investigation:

```json
{
  "correlation_id": "FIN-20260626-ABC123"
}
```

## If Risk Is High

1. Check `risk_score` and `report.risk_analysis`.
2. Review `recommendations`.
3. Confirm whether `fraud_suspicion` is also true.
4. If high risk is confirmed, route the case to manual review or compliance escalation.

## If Prompt Injection Is Detected

1. Do not rely on the incident description as-is.
2. Review `monitoring.ai_safety.prompt_injection`.
3. Keep the incident in `manual_review`.
4. Ask for a cleaned description before reprocessing.

## If PII Is Detected

1. Review `monitoring.ai_safety.pii`.
2. Avoid copying raw sensitive data into tickets or logs.
3. Mask or redact the data before sharing.
4. Keep the case under manual review if needed.

## If API Is Down

1. Check the process logs.
2. Run:

```bash
curl http://localhost:8002/health
```

3. Verify environment variables, especially Grok configuration.
4. Restart the service.

## Restart Docker

Stop containers:

```bash
docker compose down
```

Rebuild and restart:

```bash
docker compose up --build
```

## Verify Render

1. Open the Render service dashboard.
2. Check the latest deploy status.
3. Review logs for startup errors.
4. Confirm environment variables are configured.
5. Open `/health` from the Render service URL.
