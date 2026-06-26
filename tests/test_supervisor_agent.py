"""Tests for SupervisorAgent."""

from typing import Any

from app.agents.supervisor_agent import SupervisorAgent


class GraphStub:
    """Compiled graph test double."""

    def __init__(self) -> None:
        """Initialize invocation tracking."""
        self.invoked = False

    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Return a final LangGraph state."""
        self.invoked = True
        return {
            **state,
            "risk_result": {"risk_level": "high", "risk_score": 92, "reasons": ["large amount"]},
            "fraud_result": {
                "fraud_suspicion": True,
                "fraud_score": 87,
                "signals": ["new beneficiary"],
            },
            "compliance_result": {
                "compliance_status": "escalation_required",
                "required_action": "escalate_to_compliance_team",
                "reasons": ["high risk and fraud suspicion"],
            },
            "ai_safety_result": {"safe": True},
            "decision": "blocked",
            "recommendations": ["Escalate to compliance team"],
            "monitoring": {
                "correlation_id": state["correlation_id"],
                "status": "processed",
                "execution_time_ms": 1.0,
            },
            "report": {
                "summary": "High-risk incident requiring escalation.",
                "risk_analysis": {"risk_level": "high"},
                "fraud_analysis": {"fraud_suspicion": True},
                "compliance_analysis": {"compliance_status": "escalation_required"},
                "ai_safety": {"safe": True},
                "recommended_next_steps": ["Escalate to compliance team"],
                "final_status": "completed",
            },
        }


def test_supervisor_agent_passes_through_langgraph(high_risk_incident) -> None:
    """SupervisorAgent invokes the compiled LangGraph."""
    graph = GraphStub()

    SupervisorAgent(graph=graph).analyze(high_risk_incident)

    assert graph.invoked is True


def test_supervisor_agent_returns_correlation_id(high_risk_incident) -> None:
    """SupervisorAgent returns a correlation id."""
    result = SupervisorAgent(graph=GraphStub()).analyze(high_risk_incident)

    assert result["correlation_id"].startswith("FIN-")


def test_supervisor_agent_returns_decision(high_risk_incident) -> None:
    """SupervisorAgent returns a final decision."""
    result = SupervisorAgent(graph=GraphStub()).analyze(high_risk_incident)

    assert result["decision"] == "blocked"


def test_supervisor_agent_returns_monitoring(high_risk_incident) -> None:
    """SupervisorAgent returns monitoring data."""
    result = SupervisorAgent(graph=GraphStub()).analyze(high_risk_incident)

    assert "monitoring" in result
    assert result["monitoring"]["correlation_id"] == result["correlation_id"]


def test_supervisor_agent_returns_report(high_risk_incident) -> None:
    """SupervisorAgent returns a final report."""
    result = SupervisorAgent(graph=GraphStub()).analyze(high_risk_incident)

    assert result["report"]["final_status"] == "completed"


def test_supervisor_agent_full_pipeline_high_risk(high_risk_incident) -> None:
    """SupervisorAgent handles a complete high-risk graph result."""
    result = SupervisorAgent(graph=GraphStub()).analyze(high_risk_incident)

    assert result["risk_level"] == "high"
    assert result["fraud_suspicion"] is True
    assert result["compliance_status"] == "escalation_required"
    assert result["decision"] == "blocked"
    assert result["recommendations"]
