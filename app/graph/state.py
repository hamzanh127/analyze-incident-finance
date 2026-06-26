"""State definitions for the finance incident LangGraph."""

from typing import Any, TypedDict


class FinanceIncidentState(TypedDict, total=False):
    """Shared state passed between finance incident graph nodes."""

    incident: Any
    correlation_id: str
    request_id: str
    timestamp: str
    execution_time_ms: float
    risk_result: dict[str, Any]
    fraud_result: dict[str, Any]
    compliance_result: dict[str, Any]
    ai_safety_result: dict[str, Any]
    decision: str
    recommendations: list[str]
    monitoring: dict[str, Any]
    report: dict[str, Any]
    errors: list[str]
