# Release Notes

User-facing and trainer-facing summary of what each version of `finance-incident-multi-agent` delivers.

---
## v1.7.0 - LangSmith Observability UI

**Release date:** 2026-06-26

This release turns the React frontend into a full observability dashboard for the finance multi-agent workflow.

### What's New

- A LangGraph workflow view shows the full path from Client to FastAPI, Supervisor, Risk, Fraud, Compliance, Monitoring, and Report.
- A trace timeline highlights correlation ID generation, agent completion, monitoring, report generation, and final decision.
- LangSmith status is visible in the UI, including project, tracing, environment, version, run name, trace availability, and correlation ID.
- The observability panel exposes decision, risk level, execution time, telemetry flags, and trace status.
- The monitoring panel supports both legacy safety output and the newer hybrid static plus Grok safety format.
- The chat panel sends the current incident, analysis result, message, and history to `POST /chat`.
- `frontend/.env.example` documents `VITE_API_BASE_URL=http://localhost:8002`.

### What It Means for a Demo

An evaluator can submit an incident and immediately see the orchestration, safety checks, metrics, LangSmith state, correlation ID, and a contextual chat experience in one interface.

---
## v1.6.0 - LangSmith Observability

**Release date:** 2026-06-26

This release adds LangSmith as the external observability platform for the LangGraph workflow.

### What's New

- Every graph execution can be traced under the run name `finance_incident_analysis`.
- The workflow exposes distinct trace steps for Supervisor, Risk, Fraud, Compliance, Monitoring, and Report Generation.
- Trace metadata includes `correlation_id`, `request_id`, `incident_type`, `amount`, `risk_level`, `decision`, `execution_time`, `environment`, and `application_version`.
- A new `GET /observability` endpoint reports the effective LangSmith configuration.
- The Monitoring Agent response now includes a `langsmith` block showing whether traces are available.
- Tests mock LangSmith and explicitly disable external tracing by default.

### What It Means for a Demo

Run an incident through `/analyze`, copy the returned `correlation_id`, then search for that value in the LangSmith project `finance-incident-multi-agent` to inspect the exact multi-agent execution path.

---

## v1.5.0 — Grok-Based AI Monitoring

**Release date:** 2026-06-26

The Monitoring Agent is no longer limited to simple keyword lists. This release adds a second analysis layer powered by the Grok LLM, making safety decisions significantly more accurate and explainable.

### What's New

- **Two-phase safety pipeline:** every incident description now goes through (1) deterministic static checks, then (2) a Grok LLM safety review using a specialized AI Safety Agent prompt.
- **Grok detects what regex cannot:** jailbreak attempts, hallucination risk, non-compliant phrasing, subtle prompt injections, and low-confidence PII that doesn't match a fixed pattern.
- **Transparent fusion:** the `final_decision` object tells you exactly what triggered the safety flag — the static layer, Grok, or both — via the `source` field (`static` or `hybrid`) and a `reasons` list.
- **Resilient by design:** if Grok is down or returns an invalid response, the system automatically falls back to static-only mode. The `grok_safety_review` field carries `available: false` so the frontend can react accordingly.
- **Richer UI feedback:** the Monitoring Agent chat bubble now shows 8 distinct lines grouped by source — `[Static]`, `[Grok]`, `[Final]` — with coloured 🔴/🟠/🟢 labels and a badge matching the final decision.
- **88 tests, all green:** 15 new tests cover every path — Grok allow, Grok block, Grok unavailable, static override, source attribution — all using mocks, no live API calls.

### What It Means for a Demo

Submit an incident with `"ignore previous instructions"` in the description. The `[Static]` layer flags it immediately. Grok also independently classifies it as a high-risk prompt injection and returns `recommended_action: block`. The final decision shows `BLOCK` with a 🔴 badge and a `reasons` list explaining both sources of the flag.

---
## v1.6.0 - LangSmith Observability

**Release date:** 2026-06-26

This release adds LangSmith as the external observability platform for the LangGraph workflow.

### What's New

- Every graph execution can be traced under the run name `finance_incident_analysis`.
- The workflow exposes distinct trace steps for Supervisor, Risk, Fraud, Compliance, Monitoring, and Report Generation.
- Trace metadata includes `correlation_id`, `request_id`, `incident_type`, `amount`, `risk_level`, `decision`, `execution_time`, `environment`, and `application_version`.
- A new `GET /observability` endpoint reports the effective LangSmith configuration.
- The Monitoring Agent response now includes a `langsmith` block showing whether traces are available.
- Tests mock LangSmith and explicitly disable external tracing by default.

### What It Means for a Demo

Run an incident through `/analyze`, copy the returned `correlation_id`, then search for that value in the LangSmith project `finance-incident-multi-agent` to inspect the exact multi-agent execution path.

---

## v1.4.0 — Production Release

**Release date:** 2026-06-26

This release packages the project for a professional end-of-training presentation. No functional code changes were made — the focus is entirely on documentation quality and project coherence.

### What's New

- The project now has a complete and consistent documentation suite: versioning strategy, changelog, release notes, and an updated architecture document.
- The `README.md` includes a visual release timeline and a version index so any evaluator can immediately understand the project's progression.
- All documentation reflects features that are **actually implemented** — nothing is described that does not exist in the codebase.

### Why It Matters

A project without versioning documentation is difficult to evaluate, maintain, or hand over. This release ensures the project meets professional standards for traceability and presentation.

---
## v1.6.0 - LangSmith Observability

**Release date:** 2026-06-26

This release adds LangSmith as the external observability platform for the LangGraph workflow.

### What's New

- Every graph execution can be traced under the run name `finance_incident_analysis`.
- The workflow exposes distinct trace steps for Supervisor, Risk, Fraud, Compliance, Monitoring, and Report Generation.
- Trace metadata includes `correlation_id`, `request_id`, `incident_type`, `amount`, `risk_level`, `decision`, `execution_time`, `environment`, and `application_version`.
- A new `GET /observability` endpoint reports the effective LangSmith configuration.
- The Monitoring Agent response now includes a `langsmith` block showing whether traces are available.
- Tests mock LangSmith and explicitly disable external tracing by default.

### What It Means for a Demo

Run an incident through `/analyze`, copy the returned `correlation_id`, then search for that value in the LangSmith project `finance-incident-multi-agent` to inspect the exact multi-agent execution path.

---

## v1.3.0 — AI Security & Telemetry

**Release date:** 2026-06-26

The Monitoring Agent was previously decorative — it returned hardcoded placeholder values. This release makes it real.

### What's New

- **Real PII detection:** the system now detects emails, Moroccan phone numbers, Moroccan CINs, credit card numbers, IBANs, and explicitly named individuals (`nom: Hamza Nachat`). Sensitive values are **never returned** in the API response — only the type and count of matches.
- **Real prompt injection detection:** 9 known attack patterns are now detected, including `jailbreak`, `disable guardrails`, and `act as developer mode`.
- **Bilingual toxicity check:** English and French toxic terms are detected (e.g., `putain`, `connard`, `merde`).
- **Live security badge in the UI:** the Monitoring Agent chat bubble turns **red** if any security issue is found, and **green** if everything is clean.
- **Live telemetry values:** the UI now shows the real estimated token count and USD cost calculated from the submitted incident text.

### What It Means for a Demo

Submit an incident with the text `"nom: Hamza Nachat, carte: 4111111111111111"`. The Monitoring Agent will immediately flag **PII Detected: name, credit_card** with a red badge — while all other agents continue their analysis normally.

---
## v1.6.0 - LangSmith Observability

**Release date:** 2026-06-26

This release adds LangSmith as the external observability platform for the LangGraph workflow.

### What's New

- Every graph execution can be traced under the run name `finance_incident_analysis`.
- The workflow exposes distinct trace steps for Supervisor, Risk, Fraud, Compliance, Monitoring, and Report Generation.
- Trace metadata includes `correlation_id`, `request_id`, `incident_type`, `amount`, `risk_level`, `decision`, `execution_time`, `environment`, and `application_version`.
- A new `GET /observability` endpoint reports the effective LangSmith configuration.
- The Monitoring Agent response now includes a `langsmith` block showing whether traces are available.
- Tests mock LangSmith and explicitly disable external tracing by default.

### What It Means for a Demo

Run an incident through `/analyze`, copy the returned `correlation_id`, then search for that value in the LangSmith project `finance-incident-multi-agent` to inspect the exact multi-agent execution path.

---

## v1.2.0 — Agent Chat Experience

**Release date:** 2026-06-26

The interface was completely transformed from a static results dashboard into a conversational "Agent Chat" experience.

### What's New

- After submitting an incident, the form disappears and a chat interface appears.
- Each specialized agent "speaks" in sequence, with a 800 ms delay between messages, creating a realistic multi-agent conversation effect.
- A "thinking" animation (animated dots) appears while the API processes the request.
- A "New Incident" button allows resetting the flow without refreshing the page.

### Agent Message Sequence

1. **Supervisor Agent** — confirms the correlation ID received.
2. **Risk Agent** — reports risk level, score, and reasons.
3. **Fraud Agent** — reports fraud suspicion, score, and signals.
4. **Compliance Agent** — reports compliance status and required action.
5. **Monitoring Agent** — reports security and telemetry checks.
6. **Final Report** — presents the decision and recommendations.

### What It Means for a Demo

The chat interface makes the multi-agent architecture immediately understandable to a non-technical audience. Each agent's contribution is visible and attributed.

---
## v1.6.0 - LangSmith Observability

**Release date:** 2026-06-26

This release adds LangSmith as the external observability platform for the LangGraph workflow.

### What's New

- Every graph execution can be traced under the run name `finance_incident_analysis`.
- The workflow exposes distinct trace steps for Supervisor, Risk, Fraud, Compliance, Monitoring, and Report Generation.
- Trace metadata includes `correlation_id`, `request_id`, `incident_type`, `amount`, `risk_level`, `decision`, `execution_time`, `environment`, and `application_version`.
- A new `GET /observability` endpoint reports the effective LangSmith configuration.
- The Monitoring Agent response now includes a `langsmith` block showing whether traces are available.
- Tests mock LangSmith and explicitly disable external tracing by default.

### What It Means for a Demo

Run an incident through `/analyze`, copy the returned `correlation_id`, then search for that value in the LangSmith project `finance-incident-multi-agent` to inspect the exact multi-agent execution path.

---

## v1.1.0 — Frontend Dashboard

**Release date:** 2026-06-26

A React + Vite frontend was added to the project to provide a visual interface for the backend API.

### What's New

- A submission form for financial incidents with all required fields (customer ID, incident type, amount, currency, country, device, beneficiary status, description).
- A results panel displaying all fields from the `POST /analyze` response: correlation ID, risk level, fraud suspicion, compliance status, decision, recommendations, monitoring data, and the full report.
- A live metrics panel polling the `/metrics` endpoint.
- A monitoring panel displaying AI safety check values.

### What It Means for a Demo

Instead of using `curl` or Postman, an evaluator can interact with the multi-agent system through a modern web interface running at `http://localhost:5173`.

---
## v1.6.0 - LangSmith Observability

**Release date:** 2026-06-26

This release adds LangSmith as the external observability platform for the LangGraph workflow.

### What's New

- Every graph execution can be traced under the run name `finance_incident_analysis`.
- The workflow exposes distinct trace steps for Supervisor, Risk, Fraud, Compliance, Monitoring, and Report Generation.
- Trace metadata includes `correlation_id`, `request_id`, `incident_type`, `amount`, `risk_level`, `decision`, `execution_time`, `environment`, and `application_version`.
- A new `GET /observability` endpoint reports the effective LangSmith configuration.
- The Monitoring Agent response now includes a `langsmith` block showing whether traces are available.
- Tests mock LangSmith and explicitly disable external tracing by default.

### What It Means for a Demo

Run an incident through `/analyze`, copy the returned `correlation_id`, then search for that value in the LangSmith project `finance-incident-multi-agent` to inspect the exact multi-agent execution path.

---

## v1.0.0 — Backend MVP

**Release date:** 2026-06-26

The first complete, production-ready version of the backend API and multi-agent system.

### What's New

- **API:** four endpoints — `/` (status), `/health`, `/metrics`, `/analyze`.
- **Multi-agent pipeline:** `SupervisorAgent` orchestrates `RiskAgent`, `FraudAgent`, and `ComplianceAgent` through a LangGraph graph, with deterministic fallbacks if the LLM is unavailable.
- **AI safety layer:** toxicity, hallucination, prompt injection, and PII checks run on every submitted incident.
- **Observability:** every analysis produces a unique `correlation_id` (e.g., `FIN-20260626-ABC123`) for traceability across logs, metrics, and API responses.
- **Containerization:** the service can be started with a single `docker compose up --build` command.
- **CI/CD:** 9 GitHub Actions workflows validate API behavior, agent logic, LangGraph orchestration, monitoring checks, security, code coverage, Docker build, governance documents, and cloud health.
- **71 automated tests** — all deterministic, no live API calls required.

### What It Means for a Demo

The backend can be demonstrated entirely locally or via Docker, without any network dependency beyond the optional Grok LLM key. All agent responses have deterministic fallbacks, so the system always produces a valid, structured output.
