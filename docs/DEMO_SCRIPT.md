# Demo Script

## 3-Minute Oral Demo

Hello, today I will present `finance-incident-multi-agent`, a training project that demonstrates how to analyze financial incidents with a multi-agent AI architecture.

The application is built with FastAPI, Pydantic, pytest, and LangGraph. The goal is to receive a financial incident, analyze it through specialized agents, and return a structured decision with monitoring information.

First, the API exposes a simple health endpoint. When I call `/health`, the service returns `healthy`, which confirms that the application and its core agents are available.

Next, I send an incident to `POST /analyze`. The input contains the customer id, incident type, amount, currency, country, device, beneficiary status, and description. This payload is validated by Pydantic, so invalid data such as a negative amount is rejected automatically.

The analysis is orchestrated by LangGraph. The graph starts with the risk node, then moves to fraud detection, compliance review, AI safety monitoring, decision calculation, execution monitoring, and final report generation.

The RiskAgent estimates the risk level and score. The FraudAgent checks suspicious transaction signals. The ComplianceAgent evaluates AML, KYC, and escalation requirements. The MonitoringService checks safety concerns such as prompt injection and PII.

The final decision is deterministic. For example, if compliance escalation is required, the decision is `blocked`. If the risk is low and no fraud is detected, the decision is `approved`. Otherwise, the service usually returns `manual_review`.

Every response includes a `correlation_id`, which is important for traceability. The response also includes recommendations, monitoring data, and a structured report.

For observability, the project provides `/metrics`, structured logs, correlation ids, latency monitoring, token estimates, cost estimates, and safety checks.

Finally, the project includes a complete pytest suite. External AI calls are mocked in tests, which makes the test suite fast, deterministic, and safe for local development.

This project is not a production banking system. It is a professional training project showing how to structure a multi-agent backend with clear boundaries, typed schemas, observability, governance, and test coverage.
