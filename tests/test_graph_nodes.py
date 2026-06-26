"""Tests for individual LangGraph nodes."""

from app.graph import nodes
from app.services.correlation_service import generate_correlation_id


def test_risk_node_execution(monkeypatch, incident) -> None:
    """risk_node executes RiskAgent and stores risk_result."""

    class RiskStub:
        def analyze(self, incident) -> dict:
            return {"risk_level": "medium", "risk_score": 45, "reasons": ["test"]}

    monkeypatch.setattr(nodes, "RiskAgent", RiskStub)

    result = nodes.risk_node({"incident": incident})

    assert result["risk_result"]["risk_level"] == "medium"
    assert result["risk_result"]["risk_score"] == 45


def test_fraud_node_execution(monkeypatch, incident) -> None:
    """fraud_node executes FraudAgent and stores fraud_result."""

    class FraudStub:
        def analyze(self, incident) -> dict:
            return {"fraud_suspicion": True, "fraud_score": 80, "signals": ["signal"]}

    monkeypatch.setattr(nodes, "FraudAgent", FraudStub)

    result = nodes.fraud_node({"incident": incident})

    assert result["fraud_result"]["fraud_suspicion"] is True
    assert result["fraud_result"]["signals"] == ["signal"]


def test_compliance_node_execution(monkeypatch, incident) -> None:
    """compliance_node executes ComplianceAgent with previous results."""

    class ComplianceStub:
        def analyze(self, incident, risk_result, fraud_result) -> dict:
            assert risk_result["risk_level"] == "high"
            assert fraud_result["fraud_suspicion"] is True
            return {
                "compliance_status": "escalation_required",
                "required_action": "escalate_to_compliance_team",
                "reasons": ["test"],
            }

    monkeypatch.setattr(nodes, "ComplianceAgent", ComplianceStub)

    result = nodes.compliance_node(
        {
            "incident": incident,
            "risk_result": {"risk_level": "high"},
            "fraud_result": {"fraud_suspicion": True},
        }
    )

    assert result["compliance_result"]["compliance_status"] == "escalation_required"


def test_ai_safety_node_execution(monkeypatch, incident) -> None:
    """ai_safety_node executes MonitoringService and stores ai_safety_result."""

    class MonitoringServiceStub:
        def analyze_text(self, text: str) -> dict:
            assert text == incident.description
            return {"safe": True, "tokens": {"estimated_tokens": 3}}

    monkeypatch.setattr(nodes, "MonitoringService", MonitoringServiceStub)

    result = nodes.ai_safety_node({"incident": incident})

    assert result["ai_safety_result"]["safe"] is True


def test_decision_node_execution() -> None:
    """decision_node calculates decision and recommendations."""
    result = nodes.decision_node(
        {
            "risk_result": {"risk_level": "high"},
            "fraud_result": {"fraud_suspicion": True},
            "compliance_result": {"compliance_status": "compliant"},
            "ai_safety_result": {"safe": True},
        }
    )

    assert result["decision"] == "blocked"
    assert result["recommendations"]


def test_monitoring_node_execution() -> None:
    """monitoring_node stores execution monitoring state."""
    correlation_id = generate_correlation_id()

    result = nodes.monitoring_node({"correlation_id": correlation_id})

    assert result["monitoring"]["correlation_id"] == correlation_id
    assert result["monitoring"]["status"] == "processed"


def test_report_node_final_state() -> None:
    """report_node builds the final structured report."""
    state = {
        "risk_result": {"risk_level": "high"},
        "fraud_result": {"fraud_suspicion": True},
        "compliance_result": {"compliance_status": "escalation_required"},
        "ai_safety_result": {"safe": True},
        "recommendations": ["Escalate"],
        "decision": "blocked",
    }

    result = nodes.report_node(state)

    assert result["report"]["risk_analysis"] == state["risk_result"]
    assert result["report"]["fraud_analysis"] == state["fraud_result"]
    assert result["report"]["compliance_analysis"] == state["compliance_result"]
    assert result["report"]["ai_safety"] == state["ai_safety_result"]
    assert result["report"]["final_status"] == "completed"
