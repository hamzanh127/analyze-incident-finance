# Architecture

## Overview

`finance-incident-multi-agent` is a FastAPI training project for financial incident analysis. It uses specialized agents for risk, fraud, compliance, and monitoring, with LangGraph as the orchestration engine.

## Main Components

- `app/main.py`: FastAPI application factory and root endpoint.
- `app/api/`: HTTP routes for health, metrics, and incident analysis.
- `app/schemas/`: Pydantic request and response contracts.
- `app/agents/`: AI agent classes and the LangGraph-backed supervisor.
- `app/graph/`: LangGraph state, nodes, and compiled workflow.
- `app/services/`: technical services for correlation ids, metrics, logs, decisions, and Grok.
- `app/monitoring/`: deterministic observability and safety checks.

## LangGraph Flow

The workflow is:

```text
START
-> Supervisor Agent
-> Risk Agent
-> Fraud Agent
-> Compliance Agent
-> AI Safety Checks
-> Decision Engine
-> Monitoring Agent
-> Report Generation
-> END
```

`SupervisorAgent` generates a `correlation_id`, creates the initial state, invokes the compiled graph, and formats the final response.

## Observability Flow

LangSmith observes the workflow from outside the business logic. It receives traces and metadata, but it does not decide, enrich, block, approve, or alter incidents.

```text
Client
  |
  v
FastAPI
  |
  v
Supervisor (LangGraph)
  |
  v
Risk Agent
  |
  v
Fraud Agent
  |
  v
Compliance Agent
  |
  v
Monitoring Agent
  |
  v
Report
  |
  v
LangSmith Observability
```

Business decisions remain inside the LangGraph agents and decision service. LangSmith only records runs, steps, timing, and metadata such as `correlation_id`, `incident_type`, `risk_level`, and `decision`.

## Design Principles

- Keep orchestration in LangGraph.
- Keep domain analysis inside agents.
- Keep deterministic technical behavior in services.
- Keep input and output contracts in Pydantic schemas.
- Keep tests isolated from external API calls.

---

## Component Version Matrix

This table records from which project version each major component or capability was introduced.

| Component | Introduced in | Description |
|---|---|---|
| FastAPI backend (`app/`) | **v1.0.0** | Application factory, routers, Pydantic schemas |
| LangGraph orchestration (`app/graph/`) | **v1.0.0** | State, nodes, and compiled pipeline |
| `SupervisorAgent` | **v1.0.0** | Orchestrates the LangGraph graph and formats the API response |
| `RiskAgent` | **v1.0.0** | LLM-backed risk level analysis with deterministic fallback |
| `FraudAgent` | **v1.0.0** | LLM-backed fraud signal detection with deterministic fallback |
| `ComplianceAgent` | **v1.0.0** | LLM-backed AML/KYC compliance check with deterministic fallback |
| `MonitoringAgent` | **v1.0.0** | Execution telemetry — status, latency, correlation ID |
| Deterministic AI safety checks (`app/monitoring/`) | **v1.0.0** | Toxicity, hallucination, PII, prompt injection, tokens, cost |
| Correlation ID system | **v1.0.0** | `FIN-YYYYMMDD-XXXXXX` traceability identifier |
| Dockerfile & Docker Compose | **v1.0.0** | Single-command containerized execution |
| GitHub Actions CI/CD (9 workflows) | **v1.0.0** | Automated testing, coverage, security, Docker, cloud health |
| Render deployment (`render.yaml`) | **v1.0.0** | Cloud deployment target with Docker runtime |
| Governance documents | **v1.0.0** | `agent_card.json`, `RUNBOOK.md`, `GOVERNANCE.md`, `OBSERVABILITY.md` |
| React + Vite frontend (`frontend/`) | **v1.1.0** | Visual interface for submitting incidents and viewing results |
| CORS middleware | **v1.1.0** | Added to `app/main.py` to allow requests from `localhost:5173` |
| Agent Chat interface (`AgentChat.jsx`) | **v1.2.0** | Progressive conversational display of agent results |
| `AgentMessage.jsx` | **v1.2.0** | Reusable chat bubble component with status badge |
| Real PII detection (Moroccan phone, CIN, name) | **v1.3.0** | Enhanced regex patterns without returning raw sensitive values |
| Extended prompt injection patterns (9 vectors) | **v1.3.0** | Including jailbreak, disable guardrails, act as developer mode |
| French toxicity detection | **v1.3.0** | Bilingual toxic term set |
| Live security badge in UI | **v1.3.0** | Red/green badge on Monitoring Agent chat bubble |
| Versioning documentation (`docs/VERSIONING.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`) | **v1.4.0** | Full version traceability and project presentation |
| Hybrid `MonitoringService` (static + Grok pipeline) | **v1.5.0** | Two-phase safety analysis: deterministic checks then Grok LLM review |
| Grok AI safety system prompt | **v1.5.0** | Detects toxicity, prompt injection, PII, jailbreak, hallucination via LLM |
| `final_decision` object (`action`, `source`, `reasons`) | **v1.5.0** | Merged safety verdict with traceability of which layer triggered the flag |
| Fallback mode (`grok_safety_review.available: false`) | **v1.5.0** | Automatic degradation to static-only when Grok is unavailable |
| `MonitoringAgent.analyze_full()` | **v1.5.0** | New method exposing the full hybrid analysis to callers |
| `[Static]/[Grok]/[Final]` UI badges in Monitoring Agent bubble | **v1.5.0** | 🔴/🟠/🟢 colour-coded display per analysis source |
| `tests/test_monitoring_service.py` | **v1.5.0** | 15 mocked tests covering all hybrid paths and fallback scenarios |
| LangSmith observability | **v1.6.0** | External tracing for LangGraph runs, agent steps, correlation IDs, and metadata |
