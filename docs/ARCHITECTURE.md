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
-> risk_node
-> fraud_node
-> compliance_node
-> ai_safety_node
-> decision_node
-> monitoring_node
-> report_node
-> END
```

`SupervisorAgent` generates a `correlation_id`, creates the initial state, invokes the compiled graph, and formats the final response.

## Design Principles

- Keep orchestration in LangGraph.
- Keep domain analysis inside agents.
- Keep deterministic technical behavior in services.
- Keep input and output contracts in Pydantic schemas.
- Keep tests isolated from external API calls.
