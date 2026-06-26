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

## LangSmith Integration

LangSmith is used as the external observability platform for the LangGraph multi-agent workflow. It complements local monitoring by making each graph execution inspectable across runs, with a parent run named `finance_incident_analysis` and child steps for the Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.

LangSmith traces:

- the LangGraph workflow execution
- each agent step as a distinct workflow stage
- `correlation_id` and `request_id`
- incident metadata such as `incident_type` and `amount`
- operational metadata such as `environment`, `application_version`, `timestamp`, and `execution_time`
- final analysis metadata such as `risk_level` and `decision` when available

To run the project with LangSmith, configure `.env`:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=finance-incident-multi-agent
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

Then start the API normally:

```bash
uvicorn app.main:app --reload
```

If `LANGSMITH_API_KEY` is empty, tracing is disabled safely even when `LANGSMITH_TRACING=true`.

Use the observability endpoint to confirm runtime configuration:

```bash
curl http://localhost:8002/observability
```

To consult traces, open LangSmith, select the `finance-incident-multi-agent` project, and inspect runs named `finance_incident_analysis`.

To find a specific run, copy the `correlation_id` returned by `/analyze` and search for it in the LangSmith run metadata. The same value is also used as `request_id` when the API request does not provide a separate request identifier.
