"""Supervisor agent backed by the finance incident LangGraph."""

from inspect import Parameter, signature
from time import perf_counter
from typing import Any

from app.graph.graph_builder import compiled_finance_graph
from app.graph.state import FinanceIncidentState
from app.monitoring.langsmith_tracing import graph_invoke_config, trace_step, utc_timestamp
from app.schemas.incident_schema import IncidentRequest
from app.services.correlation_service import generate_correlation_id


class SupervisorAgent:
    """Invoke the compiled LangGraph and shape the API response."""

    def __init__(self, graph: Any | None = None) -> None:
        """Initialize the supervisor with an injectable compiled graph."""
        self._graph = graph or compiled_finance_graph

    def analyze(self, incident: IncidentRequest) -> dict[str, Any]:
        """Run the finance incident LangGraph and return an AnalyzeResponse payload."""
        correlation_id = generate_correlation_id()
        initial_state: FinanceIncidentState = {
            "incident": incident,
            "correlation_id": correlation_id,
            "request_id": correlation_id,
            "timestamp": utc_timestamp(),
            "errors": [],
            "_start_time": perf_counter(),  # type: ignore[typeddict-unknown-key]
        }
        try:
            final_state = trace_step(
                "Supervisor Agent",
                initial_state,
                lambda: self._invoke_graph(initial_state),
            )
            return self._build_response(correlation_id, final_state)
        except Exception as exc:
            return self._build_error_response(correlation_id, str(exc))

    def _invoke_graph(self, initial_state: FinanceIncidentState) -> FinanceIncidentState:
        """Invoke a real LangGraph graph while keeping test doubles compatible."""
        if self._invoke_accepts_config():
            return self._graph.invoke(initial_state, config=graph_invoke_config(initial_state))
        return self._graph.invoke(initial_state)

    def _invoke_accepts_config(self) -> bool:
        try:
            parameters = signature(self._graph.invoke).parameters.values()
        except (TypeError, ValueError):
            return True
        return any(
            parameter.name == "config" or parameter.kind == Parameter.VAR_KEYWORD
            for parameter in parameters
        )

    def _build_response(
        self,
        correlation_id: str,
        state: FinanceIncidentState,
    ) -> dict[str, Any]:
        risk_result = state.get("risk_result", {})
        fraud_result = state.get("fraud_result", {})
        compliance_result = state.get("compliance_result", {})
        return {
            "correlation_id": state.get("correlation_id", correlation_id),
            "risk_level": str(risk_result.get("risk_level", "medium")),
            "risk_score": int(risk_result.get("risk_score", 50)),
            "fraud_suspicion": bool(fraud_result.get("fraud_suspicion", False)),
            "fraud_score": int(fraud_result.get("fraud_score", 30)),
            "compliance_status": str(
                compliance_result.get("compliance_status", "review_required")
            ),
            "decision": str(state.get("decision", "manual_review")),
            "recommendations": list(state.get("recommendations", [])),
            "monitoring": state.get("monitoring", {}),
            "report": state.get("report", self._failed_report([])),
        }

    def _build_error_response(self, correlation_id: str, error: str) -> dict[str, Any]:
        errors = [error]
        return {
            "correlation_id": correlation_id,
            "risk_level": "medium",
            "risk_score": 50,
            "fraud_suspicion": False,
            "fraud_score": 30,
            "compliance_status": "review_required",
            "decision": "manual_review",
            "recommendations": ["Manual review required because graph orchestration failed."],
            "monitoring": {
                "correlation_id": correlation_id,
                "status": "failed",
                "execution_time_ms": 0.0,
            },
            "report": self._failed_report(errors),
        }

    def _failed_report(self, errors: list[str]) -> dict[str, Any]:
        return {
            "summary": "Finance incident graph orchestration failed.",
            "risk_analysis": {},
            "fraud_analysis": {},
            "compliance_analysis": {},
            "ai_safety": {},
            "recommended_next_steps": ["Perform manual review."],
            "final_status": "failed",
            "errors": errors,
        }
