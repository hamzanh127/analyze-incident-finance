"""Tests for analyze API endpoint."""

from typing import Any

from fastapi.testclient import TestClient

from app.api import routes
from app.main import app


class SupervisorStub:
    """Supervisor test double for API tests."""

    def analyze(self, incident: Any) -> dict[str, Any]:
        """Return a valid AnalyzeResponse payload."""
        return {
            "correlation_id": "FIN-20260626-ABC123",
            "risk_level": "medium",
            "risk_score": 50,
            "fraud_suspicion": False,
            "fraud_score": 20,
            "compliance_status": "review_required",
            "decision": "manual_review",
            "recommendations": ["Complete manual validation."],
            "monitoring": {"execution": {"status": "processed"}},
            "report": {"summary": "Manual review required.", "final_status": "completed"},
        }


def valid_payload() -> dict[str, object]:
    """Return a valid analyze request payload."""
    return {
        "customer_id": "cust_123",
        "incident_type": "wire_transfer",
        "amount": 1_500.0,
        "currency": "USD",
        "country": "US",
        "device": "mobile",
        "beneficiary_status": "new",
        "description": "Transfer to a new beneficiary requires review.",
    }


def test_analyze_with_valid_payload_returns_200() -> None:
    """POST /analyze with a valid payload returns HTTP 200."""
    routes.supervisor_agent = SupervisorStub()
    client = TestClient(app)

    response = client.post("/analyze", json=valid_payload())

    assert response.status_code == 200


def test_analyze_returns_correlation_id() -> None:
    """POST /analyze returns correlation_id."""
    routes.supervisor_agent = SupervisorStub()
    client = TestClient(app)

    response = client.post("/analyze", json=valid_payload())

    assert response.json()["correlation_id"] == "FIN-20260626-ABC123"


def test_analyze_returns_decision() -> None:
    """POST /analyze returns decision."""
    routes.supervisor_agent = SupervisorStub()
    client = TestClient(app)

    response = client.post("/analyze", json=valid_payload())

    assert response.json()["decision"] == "manual_review"


def test_analyze_returns_monitoring() -> None:
    """POST /analyze returns monitoring."""
    routes.supervisor_agent = SupervisorStub()
    client = TestClient(app)

    response = client.post("/analyze", json=valid_payload())

    assert "monitoring" in response.json()


def test_analyze_returns_report() -> None:
    """POST /analyze returns report."""
    routes.supervisor_agent = SupervisorStub()
    client = TestClient(app)

    response = client.post("/analyze", json=valid_payload())

    assert "report" in response.json()


def test_analyze_with_pii_returns_safe_false(monkeypatch) -> None:
    """POST /analyze with a description containing PII returns ai_safety.safe false."""
    from app.agents.supervisor_agent import SupervisorAgent
    from app.services.grok_service import GrokService

    class GrokServiceStub:
        def call_grok_json(self, *args, **kwargs) -> dict:
            return {
                "risk_level": "medium", "risk_score": 50, "reasons": ["mock"],
                "fraud_suspicion": False, "fraud_score": 20, "signals": ["mock"],
                "compliance_status": "review_required", "required_action": "mock",
            }
            
    monkeypatch.setattr("app.agents.risk_agent.GrokService", GrokServiceStub)
    monkeypatch.setattr("app.agents.fraud_agent.GrokService", GrokServiceStub)
    monkeypatch.setattr("app.agents.compliance_agent.GrokService", GrokServiceStub)

    routes.supervisor_agent = SupervisorAgent()
    client = TestClient(app)
    
    payload = valid_payload()
    payload["description"] = "User provided their CIN: AB123456"
    
    response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    json_resp = response.json()
    assert "report" in json_resp
    ai_safety = json_resp["report"]["ai_safety"]
    assert ai_safety["safe"] is False
    assert ai_safety["static_checks"]["pii"]["detected"] is True
