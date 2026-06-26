# Observability

## Correlation ID

Each analysis returns a `correlation_id` with this format:

```text
FIN-YYYYMMDD-XXXXXX
```

Use it to connect API responses, logs, monitoring events, and incident follow-up.

## Metrics

The service keeps in-memory metrics:

- `total_requests`
- `total_errors`
- `total_high_risk`
- `total_manual_review`
- `total_blocked`
- `average_latency_ms`

Read them with:

```bash
curl http://localhost:8002/metrics
```

## AI Safety Monitoring

The monitoring layer checks:

- toxicity
- hallucination risk
- prompt injection
- PII
- token usage
- estimated cost

These checks are deterministic and lightweight, suitable for a training project.

## Logs

`log_event()` creates structured logs with:

- `timestamp`
- `correlation_id`
- `event_type`
- `message`
- `metadata`

Avoid logging API keys, secrets, raw credentials, or unnecessary PII.
