"""Tests for LangGraph state definition."""

from app.graph.state import FinanceIncidentState


def test_finance_incident_state_contains_required_keys() -> None:
    """FinanceIncidentState exposes all expected state fields."""
    annotations = FinanceIncidentState.__annotations__

    expected_keys = {
        "incident",
        "correlation_id",
        "risk_result",
        "fraud_result",
        "compliance_result",
        "ai_safety_result",
        "decision",
        "recommendations",
        "monitoring",
        "report",
        "errors",
    }

    assert expected_keys.issubset(annotations)


def test_finance_incident_state_accepts_partial_initial_state(incident) -> None:
    """FinanceIncidentState can represent the graph initial state."""
    state: FinanceIncidentState = {
        "incident": incident,
        "correlation_id": "FIN-20260626-ABC123",
        "errors": [],
    }

    assert state["incident"] == incident
    assert state["correlation_id"] == "FIN-20260626-ABC123"
    assert state["errors"] == []
