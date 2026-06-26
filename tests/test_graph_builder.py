"""Tests for finance incident LangGraph builder."""

from app.graph import nodes
from app.graph.graph_builder import build_finance_incident_graph
from app.services.correlation_service import generate_correlation_id


def test_finance_incident_graph_executes(monkeypatch, high_risk_incident) -> None:
    """The compiled finance incident graph executes the expected pipeline."""

    class RiskStub:
        def analyze(self, incident) -> dict:
            return {"risk_level": "high", "risk_score": 90, "reasons": ["large amount"]}

    class FraudStub:
        def analyze(self, incident) -> dict:
            return {"fraud_suspicion": True, "fraud_score": 80, "signals": ["new beneficiary"]}

    class ComplianceStub:
        def analyze(self, incident, risk_result, fraud_result) -> dict:
            return {
                "compliance_status": "escalation_required",
                "required_action": "escalate_to_compliance_team",
                "reasons": ["high risk fraud"],
            }

    monkeypatch.setattr(nodes, "RiskAgent", RiskStub)
    monkeypatch.setattr(nodes, "FraudAgent", FraudStub)
    monkeypatch.setattr(nodes, "ComplianceAgent", ComplianceStub)

    graph = build_finance_incident_graph()
    result = graph.invoke(
        {
            "incident": high_risk_incident,
            "correlation_id": generate_correlation_id(),
            "errors": [],
        }
    )

    assert result["risk_result"]["risk_level"] == "high"
    assert result["fraud_result"]["fraud_suspicion"] is True
    assert result["compliance_result"]["compliance_status"] == "escalation_required"
    assert result["decision"] == "blocked"
    assert result["monitoring"]["status"] == "processed"
    assert result["report"]["final_status"] == "completed"
