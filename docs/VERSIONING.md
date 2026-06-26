# Versioning Strategy

This document describes the versioning policy applied to the `finance-incident-multi-agent` project.

---

## Semantic Versioning

The project follows [Semantic Versioning 2.0.0](https://semver.org/) — `MAJOR.MINOR.PATCH`.

| Segment | When to increment | Example |
|---|---|---|
| **MAJOR** | Breaking change to the public API or data contracts | `2.0.0` |
| **MINOR** | New backward-compatible feature or module | `1.1.0` |
| **PATCH** | Bug fix, refactor, or documentation correction | `1.0.1` |

---

## Version History

### v1.0.0 — Backend MVP

**Goal:** Establish a production-grade Python backend with FastAPI and a multi-agent orchestration pipeline.

**What was introduced:**
- FastAPI application with `/`, `/health`, `/metrics`, and `/analyze` endpoints.
- `SupervisorAgent` orchestrating `RiskAgent`, `FraudAgent`, and `ComplianceAgent` via LangGraph.
- Pydantic schemas for strict input/output validation.
- Deterministic monitoring checks: toxicity, hallucination, prompt injection, PII, token and cost estimation.
- Correlation ID system (`FIN-YYYYMMDD-XXXXXX`).
- Dockerfile and `docker-compose.yml` for containerized deployment.
- `render.yaml` configuration for cloud deployment on Render.
- GitHub Actions CI/CD pipeline (9 workflows).
- Full test suite with 71 passing tests.
- Governance documentation: `agent_card.json`, `RUNBOOK.md`, `GOVERNANCE.md`, `OBSERVABILITY.md`.

---

### v1.1.0 — Frontend Dashboard

**Goal:** Add a React + Vite frontend to visualize the multi-agent architecture and its results.

**What was introduced:**
- `frontend/` directory with a full Vite + React project.
- `IncidentForm.jsx`: form for submitting a financial incident.
- `ResultDashboard.jsx`: structured display of all analysis fields.
- `MetricsPanel.jsx`: polling display of `/metrics`.
- `MonitoringPanel.jsx`: display of AI safety values.
- CORS middleware added to the FastAPI backend (`app/main.py`).
- API client (`frontend/src/api.js`) for `POST /analyze`, `GET /health`, `GET /metrics`.

---

### v1.2.0 — Agent Chat Experience

**Goal:** Replace the static dashboard with an immersive "Agent Chat" interface for a compelling demo.

**What was introduced:**
- `AgentChat.jsx`: replaces `ResultDashboard`, orchestrates progressive message display.
- `AgentMessage.jsx`: individual chat bubble component with avatar, agent name, status badge, and content.
- Progressive reveal with 800 ms delay between agent messages (Supervisor → Risk → Fraud → Compliance → Monitoring → Final Report).
- "Thinking" animation while the API call is in progress.
- "New Incident" button to reset the form after an analysis.
- Dark-mode-ready CSS animations (`animate-fade-in`, `thinking-bubble`).

---

### v1.3.0 — AI Security & Telemetry

**Goal:** Make the Monitoring Agent fully functional with real security checks and connect live values to the frontend.

**What was introduced:**
- **PII Detection** enhanced with Moroccan phone numbers (`+212`/`0`), CIN, explicit name patterns (`nom:`, `client:`), and `matches_count` in the response.
- **Prompt Injection** pattern list expanded to 9 attack vectors: `jailbreak`, `disable guardrails`, `act as developer mode`, etc.
- **Toxicity** extended with French toxic terms (`merde`, `putain`, `connard`, etc.).
- `detect_pii` now returns `{"detected": bool, "types": [...], "matches_count": int}` without exposing raw matched values.
- `MonitoringService.analyze_text()` returns `safe: false` when toxicity is unsafe, prompt injection is detected, or PII is detected.
- Frontend Monitoring Agent bubble reads live values from `report.ai_safety`: real Toxicity/PII/Injection status, token count, estimated cost.
- Status badge turns **red** on any security issue, **green** when all checks pass.
- New unit tests covering all new detection patterns (71 total, all passing).

---

### v1.4.0 — Production Release

**Goal:** Package the project for a professional end-of-training presentation and production handover.

**What is targeted:**
- Complete versioning documentation (`VERSIONING.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`).
- Updated `ARCHITECTURE.md` with per-component version tracking.
- Updated `README.md` with a "Release Timeline" and "Project Versions" section.
- Final review confirming all CI badges are green and all 71 tests pass.
- Project ready for a live demonstration to evaluators.

---

### v1.5.0 — Grok-Based AI Monitoring

**Goal:** Upgrade the Monitoring Agent from a purely static rule engine to a hybrid intelligence layer that combines deterministic checks with Grok LLM-powered safety analysis.

**What was introduced:**
- `MonitoringService.analyze_text()` refactored as a two-phase pipeline:
  1. **Static checks** — `toxicity_checker`, `prompt_injection_checker`, `pii_checker`, `token_monitor`, `cost_monitor` (deterministic, always run).
  2. **Grok AI safety review** — LLM call with a specialized system prompt detecting toxicity, prompt injection, PII, jailbreak, hallucination, and non-compliant requests.
- New output structure: `{ safe, static_checks, grok_safety_review, final_decision, metrics }`.
- **Fusion rules**: static prompt injection or PII always forces `safe = false`; Grok `block` or `blocked` also forces `safe = false`.
- **`final_decision`** carries `action` (`allow/sanitize/block/manual_review`), `source` (`static/hybrid`), and `reasons`.
- **Graceful fallback**: if Grok is unavailable, `grok_safety_review` = `{ available: false, error: "..." }` and `final_decision` is based solely on static checks.
- `MonitoringAgent.analyze_full(text)` added to expose the full hybrid analysis.
- `grok_safety_review_enabled` flag added to `OBSERVABILITY_FLAGS`.
- Frontend Monitoring Agent bubble updated to display 8 distinct fields: `[Static]` Toxicity / Prompt Injection / PII, `[Grok]` Overall Risk / Recommended Action, `[Final]` Decision, Tokens, Cost.
- Coloured badges: 🔴 Blocked, 🟠 Warning, 🟢 All Clear.
- New test file `tests/test_monitoring_service.py` — 15 tests covering all hybrid paths, fallbacks, and merge rules. All mocked — no live Grok calls.


### v1.6.0 - LangSmith Observability

**Goal:** Add external observability for the LangGraph multi-agent workflow without changing business logic.

**What was introduced:**
- LangSmith tracing configuration through `.env` and `app/config.py`.
- Parent run name `finance_incident_analysis` for graph executions.
- Distinct trace steps for Supervisor Agent, Risk Agent, Fraud Agent, Compliance Agent, Monitoring Agent, and Report Generation.
- Trace metadata covering correlation, request, incident, decision, execution, environment, version, and timestamp fields.
- `GET /observability` endpoint for runtime visibility.
- Monitoring response LangSmith status block.
- Mocked tests that never call LangSmith servers.

---
## Branching & Release Convention

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code |
| `feature/*` | New feature development |
| `fix/*` | Bug fixes |

Each version is tagged on `main` with an annotated Git tag:

```bash
git tag -a v1.3.0 -m "v1.3.0 — AI Security & Telemetry"
git push origin v1.3.0
```
