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
