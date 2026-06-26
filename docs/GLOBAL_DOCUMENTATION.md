# Global Documentation

## Project Overview

`finance-incident-multi-agent` is a finance incident analysis platform built around a multi-agent AI workflow. It analyzes suspicious transfers, unusual transactions, new beneficiary risks, AML/KYC concerns, fraud signals, and cases requiring human review.

The project now includes:

- FastAPI backend
- LangGraph orchestration
- Grok-powered agents
- Supervisor, Risk, Fraud, Compliance and Monitoring agents
- Hybrid AI monitoring with static checks and Grok safety review
- LangSmith observability
- React + Vite supervision frontend
- Grok-backed contextual chat
- Docker, Render and GitHub Actions support

## Business Goal

The platform helps an analyst understand how an incident moves through a finance decision workflow:

```text
Incident submitted
-> Supervisor starts the workflow
-> Risk Agent evaluates financial exposure
-> Fraud Agent evaluates fraud signals
-> Compliance Agent evaluates AML/KYC status
-> Monitoring Agent evaluates safety and telemetry
-> Final report and decision are generated
-> LangSmith observes the execution
```

Every analysis returns a `correlation_id`, allowing the same incident to be followed across the API response, logs, metrics, frontend views and LangSmith traces.

## Main User Experience

The frontend is now a supervision platform, not a generic dashboard.

Pages:

- `Dashboard`: global platform health and finance statistics.
- `Incident Analysis`: incident form, agent execution animation and final decision summary.
- `AI Agent Chat`: Grok-backed assistant that answers questions about the current incident.
- `Monitoring`: security checks, Grok AI safety review, telemetry and final security decision.
- `LangGraph`: animated workflow view for each agent node.
- `Observability`: correlation ID, logs, metrics, LangSmith status, run name, version and environment.

## AI Agent Chat

The chat is connected to the backend endpoint `POST /chat`.

It sends:

- `message`
- `incident`
- `analysis_result`
- `history`

The backend uses Grok to answer in the context of the current finance incident. Quick actions include:

- Explain Risk
- Explain Fraud
- Explain Compliance
- Explain Decision
- Summarize Incident
- Generate Executive Summary
- Explain Monitoring
- Explain LangGraph Workflow

## Observability Model

The project uses two complementary observability layers:

- `MonitoringAgent`: application-level execution status, latency, safety checks and telemetry returned to the API client.
- `LangSmith`: external trace platform observing LangGraph runs and agent steps.

LangSmith does not participate in business decisions. It observes the workflow and records metadata such as `correlation_id`, `incident_type`, `risk_level`, `decision`, `environment`, `version` and `execution_time`.

## Version Summary

| Version | Summary |
|---|---|
| `v1.0.0` | Backend MVP with FastAPI, LangGraph, agents, Docker and CI/CD |
| `v1.1.0` | Initial React dashboard |
| `v1.2.0` | Agent chat-style frontend experience |
| `v1.3.0` | Real AI security and telemetry checks |
| `v1.4.0` | Production release documentation |
| `v1.5.0` | Hybrid static + Grok monitoring |
| `v1.6.0` | LangSmith backend observability |
| `v1.7.0` | Observability-focused frontend panels |
| `v1.8.0` | Grok-backed `/chat`, full supervision frontend and documentation |

## Running The Project

Backend:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Docker:

```bash
docker compose up --build
```

If Docker cannot connect to `dockerDesktopLinuxEngine`, start Docker Desktop first and verify:

```powershell
docker version
```

## Important Environment Variables

```text
GROK_API_KEY=
GROK_MODEL=grok-2-latest
GROK_API_BASE_URL=https://api.x.ai/v1

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=finance-incident-multi-agent
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

VITE_API_BASE_URL=http://localhost:8002
```

Never commit real API keys. `.env.example` must only contain placeholders.
