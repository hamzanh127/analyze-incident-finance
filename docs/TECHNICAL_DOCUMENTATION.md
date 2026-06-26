# Technical Documentation

## Architecture

```text
React + Vite Frontend
  |
  | HTTP
  v
FastAPI Backend
  |
  v
SupervisorAgent
  |
  v
LangGraph compiled workflow
  |
  +-> RiskAgent -> Grok
  +-> FraudAgent -> Grok
  +-> ComplianceAgent -> Grok
  +-> MonitoringAgent -> static checks + Grok safety review
  +-> Report Generation
  |
  v
LangSmith tracing observes runs and metadata
```

## Backend Modules

| Path | Role |
|---|---|
| `app/main.py` | FastAPI application factory, CORS and router registration |
| `app/api/routes.py` | `/analyze` and `/chat` routes |
| `app/api/health.py` | Health endpoint |
| `app/api/metrics.py` | In-memory metrics endpoint |
| `app/api/observability.py` | LangSmith status endpoint |
| `app/agents/` | Supervisor, Risk, Fraud, Compliance and Monitoring agents |
| `app/graph/` | LangGraph state, nodes and graph builder |
| `app/monitoring/` | Safety checks, telemetry, LangSmith helpers |
| `app/services/grok_service.py` | OpenAI-compatible Grok client |
| `app/schemas/` | Pydantic request and response models |

## API Endpoints

### `POST /analyze`

Runs the complete finance incident workflow.

Input:

```json
{
  "customer_id": "cust_123",
  "incident_type": "wire_transfer",
  "amount": 12500,
  "currency": "USD",
  "country": "US",
  "device": "mobile",
  "beneficiary_status": "new",
  "description": "Unauthorized transfer to a new beneficiary."
}
```

Output includes:

- `correlation_id`
- `risk_level`
- `risk_score`
- `fraud_suspicion`
- `fraud_score`
- `compliance_status`
- `decision`
- `recommendations`
- `monitoring`
- `report`

### `POST /chat`

Uses Grok to answer contextual questions about the current incident.

Input:

```json
{
  "message": "Explain Fraud",
  "incident": {},
  "analysis_result": {},
  "history": [
    { "role": "user", "content": "Explain Fraud" }
  ]
}
```

Output:

```json
{
  "message": "Grok-generated answer...",
  "provider": "grok"
}
```

If Grok is not configured, the endpoint returns `503`.

### `GET /observability`

Returns LangSmith runtime status:

```json
{
  "langsmith_enabled": true,
  "project": "finance-incident-multi-agent",
  "tracing": true,
  "environment": "local",
  "version": "1.8.0"
}
```

## Frontend Modules

| Path | Role |
|---|---|
| `frontend/src/App.jsx` | Main supervision shell, pages, shared state and workflow animation |
| `frontend/src/api.js` | API client for `/analyze`, `/chat`, `/health`, `/metrics`, `/observability` |
| `frontend/src/components/AgentChat.jsx` | Grok-backed chat UI |
| `frontend/src/components/IncidentForm.jsx` | Incident submission form |
| `frontend/src/styles.css` | Dark supervision UI, sidebar, panels, workflow and responsive layout |

## Frontend State Flow

1. The user submits an incident in `Incident Analysis`.
2. `App.jsx` calls `analyzeIncident()`.
3. The frontend animates agent stages while the backend executes LangGraph.
4. The response is stored as `analysisResult`.
5. Dashboard, Monitoring, LangGraph and Observability pages read from the same state.
6. `AI Agent Chat` sends `incident`, `analysis_result` and `history` to `/chat`.

## Grok Integration

`GrokService` reads:

```text
GROK_API_KEY
GROK_MODEL
GROK_API_BASE_URL
```

It provides:

- `call_grok()` for plain text responses.
- `call_grok_json()` for strict JSON responses used by agents and monitoring.

The chat endpoint uses `call_grok()` because it returns natural language explanations.

## LangSmith Integration

LangSmith is configured through:

```text
LANGSMITH_TRACING
LANGSMITH_API_KEY
LANGSMITH_PROJECT
LANGSMITH_ENDPOINT
```

Tracing is considered enabled only when tracing is true and an API key exists. Tests disable LangSmith by default to avoid external calls.

## Testing

Backend:

```bash
python -m pytest -q
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

Important test guarantees:

- `/chat` tests mock Grok.
- LangSmith tests do not contact LangSmith servers.
- Analyze tests use stubs/mocks for external LLM behavior.

## Deployment

Local backend:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002
```

Docker:

```bash
docker build -t finance-incident-agent .
docker run -p 8002:8002 --env-file .env finance-incident-agent
```

Frontend:

```bash
cd frontend
npm run dev
```

Render uses `render.yaml` and the Docker runtime. Configure production secrets in Render environment variables, never in repository files.
