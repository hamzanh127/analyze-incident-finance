# Changelog

All notable changes to `finance-incident-multi-agent` are documented here.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions and adheres to [Semantic Versioning](https://semver.org/).

---
## [1.8.0] - 2026-06-26 - Grok Chat & Supervision Documentation

### Added
- `POST /chat` endpoint backed by `GrokService.call_grok()` for contextual finance incident answers.
- `app/schemas/chat_schema.py` with typed chat request, history and response contracts.
- `tests/test_chat_api.py` covering Grok-backed chat and Grok unavailable scenarios with mocks.
- Full React supervision platform with Dashboard, Incident Analysis, AI Agent Chat, Monitoring, LangGraph and Observability pages.
- `lucide-react` frontend icons.
- `docs/GLOBAL_DOCUMENTATION.md` describing the full project, user experience and version history.
- `docs/TECHNICAL_DOCUMENTATION.md` describing architecture, endpoints, modules, state flow, tests and deployment.

### Changed
- Frontend chat now calls the backend `/chat` route and no longer returns fixed local answers.
- Application version updated to `1.8.0`.
- README expanded with frontend supervision pages, `/chat`, Docker troubleshooting and documentation links.

---

## [1.7.0] - 2026-06-26 - LangSmith Observability UI

### Added
- React observability dashboard for LangGraph workflow, agent timeline, LangSmith status, correlation IDs, metrics, monitoring, and final analysis report.
- Connected `AgentChat` that sends message, incident, analysis result, and chat history to `POST /chat`.
- `frontend/.env.example` with `VITE_API_BASE_URL=http://localhost:8002`.

### Changed
- Frontend API client now uses `import.meta.env.VITE_API_BASE_URL` with a localhost fallback.
- Metrics, monitoring, LangSmith, and observability panels tolerate missing backend fields and disabled LangSmith tracing.

---
## [1.6.0] - 2026-06-26 - LangSmith Observability

### Added
- LangSmith dependencies and `.env.example` configuration for `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT`.
- `app/config.py`: automatic `.env` loading and effective LangSmith enablement only when an API key is present.
- `app/monitoring/langsmith_tracing.py`: centralized LangSmith status, metadata, graph config, and trace wrappers.
- LangGraph run name `finance_incident_analysis` with metadata for `correlation_id`, `request_id`, `incident_type`, `amount`, `environment`, `version`, and `timestamp`.
- Distinct LangSmith workflow steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- `GET /observability` endpoint exposing LangSmith runtime status.
- Monitoring result `langsmith` block indicating whether tracing is enabled and traceable.
- `tests/test_langsmith.py`: mocked LangSmith tests with no external server calls.

### Changed
- LangGraph node names now use human-readable agent/workflow labels for clearer traces.
- Pytest setup disables LangSmith by default to keep the test suite deterministic and offline.
- Documentation updated across `README.md`, `docs/OBSERVABILITY.md`, and `docs/ARCHITECTURE.md`.

---

## [1.5.0] — 2026-06-26 — Grok-Based AI Monitoring

### Added
- `app/monitoring/monitoring_service.py`: two-phase hybrid pipeline — static checks followed by a Grok LLM safety review.
- Grok AI safety system prompt covering: toxicity, prompt injection, PII, jailbreak, hallucination, non-compliant requests.
- New output structure for `analyze_text()`: `{ safe, static_checks, grok_safety_review, final_decision, metrics }`.
- `final_decision` object: `{ safe, action, source, reasons }` — `source` is `static` or `hybrid`.
- Graceful fallback: `grok_safety_review = { available: false, error: "..." }` when Grok is unreachable.
- `MonitoringAgent.analyze_full(text)` — new method exposing the full hybrid analysis result.
- `grok_safety_review_enabled: True` added to `OBSERVABILITY_FLAGS`.
- `AgentChat.jsx`: Monitoring Agent bubble displays 8 fields — `[Static]` Toxicity / Prompt Injection / PII, `[Grok]` Overall Risk / Recommended Action, `[Final]` Decision, Tokens, Cost.
- Coloured badges: 🔴 Blocked / 🟠 Warning / 🟢 All Clear.
- `tests/test_monitoring_service.py`: 15 new tests covering all hybrid paths, fallback, and merge rules (all mocked — no live Grok calls).

### Changed
- `app/graph/nodes.py`: `_fallback_ai_safety()` updated to return the new nested structure.
- `tests/test_graph_nodes.py`: `ai_safety_node` test updated to assert on `static_checks`, `grok_safety_review`, and `final_decision`.
- `tests/test_analyze_api.py`: E2E PII assertion updated to use the `static_checks.pii` nested path.
- `tests/test_monitoring_agent.py`: new tests for `analyze_full` and `grok_safety_review_enabled` flag.

---
## [1.6.0] - 2026-06-26 - LangSmith Observability

### Added
- LangSmith dependencies and `.env.example` configuration for `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT`.
- `app/config.py`: automatic `.env` loading and effective LangSmith enablement only when an API key is present.
- `app/monitoring/langsmith_tracing.py`: centralized LangSmith status, metadata, graph config, and trace wrappers.
- LangGraph run name `finance_incident_analysis` with metadata for `correlation_id`, `request_id`, `incident_type`, `amount`, `environment`, `version`, and `timestamp`.
- Distinct LangSmith workflow steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- `GET /observability` endpoint exposing LangSmith runtime status.
- Monitoring result `langsmith` block indicating whether tracing is enabled and traceable.
- `tests/test_langsmith.py`: mocked LangSmith tests with no external server calls.

### Changed
- LangGraph node names now use human-readable agent/workflow labels for clearer traces.
- Pytest setup disables LangSmith by default to keep the test suite deterministic and offline.
- Documentation updated across `README.md`, `docs/OBSERVABILITY.md`, and `docs/ARCHITECTURE.md`.

---

## [1.4.0] — 2026-06-26 — Production Release

### Added
- `docs/VERSIONING.md`: semantic versioning strategy and per-version objectives.
- `docs/CHANGELOG.md`: this file — chronological feature log.
- `docs/RELEASE_NOTES.md`: user-facing summary of each version's highlights.
- `docs/ARCHITECTURE.md` updated with per-component version introduction tracking.
- `README.md` updated with "Project Versions" and "Release Timeline" sections.

---
## [1.6.0] - 2026-06-26 - LangSmith Observability

### Added
- LangSmith dependencies and `.env.example` configuration for `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT`.
- `app/config.py`: automatic `.env` loading and effective LangSmith enablement only when an API key is present.
- `app/monitoring/langsmith_tracing.py`: centralized LangSmith status, metadata, graph config, and trace wrappers.
- LangGraph run name `finance_incident_analysis` with metadata for `correlation_id`, `request_id`, `incident_type`, `amount`, `environment`, `version`, and `timestamp`.
- Distinct LangSmith workflow steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- `GET /observability` endpoint exposing LangSmith runtime status.
- Monitoring result `langsmith` block indicating whether tracing is enabled and traceable.
- `tests/test_langsmith.py`: mocked LangSmith tests with no external server calls.

### Changed
- LangGraph node names now use human-readable agent/workflow labels for clearer traces.
- Pytest setup disables LangSmith by default to keep the test suite deterministic and offline.
- Documentation updated across `README.md`, `docs/OBSERVABILITY.md`, and `docs/ARCHITECTURE.md`.

---

## [1.3.0] — 2026-06-26 — AI Security & Telemetry

### Added
- `app/monitoring/pii_checker.py`: Moroccan phone regex (`+212`/`0` + operator prefix), CIN pattern (`1–2 letters + 4–6 digits`), explicit name pattern (`nom:`, `name:`, `client:`).
- `detect_pii()` now returns `matches_count` in addition to `detected` and `types`.
- `app/monitoring/prompt_injection_checker.py`: added 5 new attack patterns — `forget all instructions`, `show hidden prompt`, `disable guardrails`, `act as developer mode`, `jailbreak`.
- `app/monitoring/toxicity_checker.py`: added French toxic terms — `merde`, `putain`, `connard`, `salaud`, `con`, `idiot`, `stupid`.
- `MonitoringService.analyze_text()` returns `safe: false` when any security check fails.
- `AgentChat.jsx`: Monitoring Agent bubble now reads real values from `report.ai_safety`.
- Red/green status badge on the Monitoring Agent chat bubble based on security outcome.
- `tests/test_pii_checker.py`: added tests for CIN, Moroccan phone, explicit name, and `matches_count`.
- `tests/test_toxicity_checker.py`: added test for French toxic text.
- `tests/test_analyze_api.py`: added E2E test verifying that a CIN in the description returns `ai_safety.safe: false`.

### Fixed
- `AgentChat.jsx`: closure bug in `setInterval` causing `TypeError: Cannot read properties of undefined (reading 'id')` — fixed by capturing `sequence[step]` before calling `setMessages`.

---
## [1.6.0] - 2026-06-26 - LangSmith Observability

### Added
- LangSmith dependencies and `.env.example` configuration for `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT`.
- `app/config.py`: automatic `.env` loading and effective LangSmith enablement only when an API key is present.
- `app/monitoring/langsmith_tracing.py`: centralized LangSmith status, metadata, graph config, and trace wrappers.
- LangGraph run name `finance_incident_analysis` with metadata for `correlation_id`, `request_id`, `incident_type`, `amount`, `environment`, `version`, and `timestamp`.
- Distinct LangSmith workflow steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- `GET /observability` endpoint exposing LangSmith runtime status.
- Monitoring result `langsmith` block indicating whether tracing is enabled and traceable.
- `tests/test_langsmith.py`: mocked LangSmith tests with no external server calls.

### Changed
- LangGraph node names now use human-readable agent/workflow labels for clearer traces.
- Pytest setup disables LangSmith by default to keep the test suite deterministic and offline.
- Documentation updated across `README.md`, `docs/OBSERVABILITY.md`, and `docs/ARCHITECTURE.md`.

---

## [1.2.0] — 2026-06-26 — Agent Chat Experience

### Added
- `frontend/src/components/AgentChat.jsx`: full chat-style analysis display replacing `ResultDashboard`.
- `frontend/src/components/AgentMessage.jsx`: reusable chat bubble with avatar, agent name, status badge, content, and details list.
- Progressive message reveal: 800 ms delay between each agent's message (Supervisor → Risk → Fraud → Compliance → Monitoring → Final Report).
- "Thinking" animation (animated dots) while the API call is pending.
- `App.jsx` updated: form collapses after submission; "New Incident" button resets the flow.
- CSS additions: `.chat-container`, `.chat-message`, `.chat-bubble`, `.chat-avatar`, `.animate-fade-in`, `.thinking-bubble`.

### Changed
- `App.jsx`: replaced `ResultDashboard` with `AgentChat`; added `showForm` state for form/chat toggle.

---
## [1.6.0] - 2026-06-26 - LangSmith Observability

### Added
- LangSmith dependencies and `.env.example` configuration for `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT`.
- `app/config.py`: automatic `.env` loading and effective LangSmith enablement only when an API key is present.
- `app/monitoring/langsmith_tracing.py`: centralized LangSmith status, metadata, graph config, and trace wrappers.
- LangGraph run name `finance_incident_analysis` with metadata for `correlation_id`, `request_id`, `incident_type`, `amount`, `environment`, `version`, and `timestamp`.
- Distinct LangSmith workflow steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- `GET /observability` endpoint exposing LangSmith runtime status.
- Monitoring result `langsmith` block indicating whether tracing is enabled and traceable.
- `tests/test_langsmith.py`: mocked LangSmith tests with no external server calls.

### Changed
- LangGraph node names now use human-readable agent/workflow labels for clearer traces.
- Pytest setup disables LangSmith by default to keep the test suite deterministic and offline.
- Documentation updated across `README.md`, `docs/OBSERVABILITY.md`, and `docs/ARCHITECTURE.md`.

---

## [1.1.0] — 2026-06-26 — Frontend Dashboard

### Added
- `frontend/` directory: full Vite + React 18 project.
- `frontend/src/components/IncidentForm.jsx`: financial incident submission form with all required fields.
- `frontend/src/components/ResultDashboard.jsx`: structured display of all API response fields.
- `frontend/src/components/MetricsPanel.jsx`: polling display of `/metrics` endpoint data.
- `frontend/src/components/MonitoringPanel.jsx`: display of AI safety monitoring values.
- `frontend/src/api.js`: API client for `analyzeIncident`, `getHealth`, `getMetrics`.
- `frontend/src/styles.css`: design system with dark theme, card components, status badges, grid layout.

### Changed
- `app/main.py`: added `CORSMiddleware` for `http://localhost:5173` and `http://127.0.0.1:5173`.

---
## [1.6.0] - 2026-06-26 - LangSmith Observability

### Added
- LangSmith dependencies and `.env.example` configuration for `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT`.
- `app/config.py`: automatic `.env` loading and effective LangSmith enablement only when an API key is present.
- `app/monitoring/langsmith_tracing.py`: centralized LangSmith status, metadata, graph config, and trace wrappers.
- LangGraph run name `finance_incident_analysis` with metadata for `correlation_id`, `request_id`, `incident_type`, `amount`, `environment`, `version`, and `timestamp`.
- Distinct LangSmith workflow steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- `GET /observability` endpoint exposing LangSmith runtime status.
- Monitoring result `langsmith` block indicating whether tracing is enabled and traceable.
- `tests/test_langsmith.py`: mocked LangSmith tests with no external server calls.

### Changed
- LangGraph node names now use human-readable agent/workflow labels for clearer traces.
- Pytest setup disables LangSmith by default to keep the test suite deterministic and offline.
- Documentation updated across `README.md`, `docs/OBSERVABILITY.md`, and `docs/ARCHITECTURE.md`.

---

## [1.0.0] — 2026-06-26 — Backend MVP

### Added
- `app/main.py`: FastAPI application factory with root, health, metrics, and analyze routers.
- `app/api/routes.py`: `POST /analyze` endpoint with `AnalyzeRequest` / `AnalyzeResponse` schemas.
- `app/agents/supervisor_agent.py`: orchestrator generating correlation IDs and formatting responses.
- `app/agents/risk_agent.py`: LLM-backed risk analysis via Grok (with local fallback).
- `app/agents/fraud_agent.py`: LLM-backed fraud detection via Grok (with local fallback).
- `app/agents/compliance_agent.py`: LLM-backed AML/KYC compliance evaluation via Grok (with local fallback).
- `app/agents/monitoring_agent.py`: execution telemetry and observability tracking.
- `app/graph/`: LangGraph state (`FinanceIncidentState`), nodes, and compiled graph builder.
- `app/monitoring/`: deterministic checks — toxicity, hallucination, prompt injection, PII, token monitor, cost monitor, latency monitor, health monitor, metrics collector.
- `app/services/`: correlation service, decision service, Grok service, metrics service, log service.
- `app/schemas/`: Pydantic request and response models.
- `Dockerfile` and `docker-compose.yml` for containerized local execution.
- `render.yaml` for cloud deployment on Render.
- `.github/workflows/`: 9 GitHub Actions workflows — CI, API tests, agent tests, LangGraph tests, monitoring tests, governance tests, coverage, Docker build, security scan.
- `agent_card.json`: agent identity and capability manifest.
- `docs/RUNBOOK.md`, `docs/GOVERNANCE.md`, `docs/OBSERVABILITY.md`, `docs/API_DOC.md`, `docs/TESTING.md`, `docs/DEMO_SCRIPT.md`, `docs/ARCHITECTURE.md`.
- Initial test suite: 71 unit and integration tests.
