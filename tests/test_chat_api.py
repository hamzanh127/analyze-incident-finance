"""Tests for the Grok-backed chat endpoint."""

from fastapi.testclient import TestClient

from app.api import routes
from app.main import app
from app.services.grok_service import GrokServiceError


class GrokChatStub:
    """Grok test double for chat API tests."""

    def __init__(self) -> None:
        self.system_prompt = ""
        self.user_prompt = ""

    def call_grok(self, system_prompt: str, user_prompt: str) -> str:
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        return "Fraud risk is elevated because the beneficiary is new and the amount is unusual."


def chat_payload() -> dict[str, object]:
    """Return a valid contextual chat request."""
    return {
        "message": "Explain Fraud",
        "incident": {
            "incident_type": "wire_transfer",
            "amount": 15000,
            "currency": "USD",
            "beneficiary_status": "new",
        },
        "analysis_result": {
            "correlation_id": "FIN-20260626-ABC123",
            "fraud_suspicion": True,
            "fraud_score": 82,
            "decision": "manual_review",
        },
        "history": [{"role": "user", "content": "Explain Fraud"}],
    }


def test_chat_endpoint_uses_grok(monkeypatch) -> None:
    """POST /chat returns a Grok-generated response."""
    stub = GrokChatStub()
    monkeypatch.setattr(routes, "grok_service", stub)
    client = TestClient(app)

    response = client.post("/chat", json=chat_payload())

    assert response.status_code == 200
    assert response.json()["provider"] == "grok"
    assert "Fraud risk is elevated" in response.json()["message"]
    assert "Finance Incident Multi-Agent" in stub.system_prompt
    assert "Explain Fraud" in stub.user_prompt
    assert "analysis_result" in stub.user_prompt


def test_chat_endpoint_returns_503_when_grok_unavailable(monkeypatch) -> None:
    """POST /chat surfaces Grok availability errors as 503 responses."""

    class FailingGrokStub:
        def call_grok(self, system_prompt: str, user_prompt: str) -> str:
            raise GrokServiceError("GROK_API_KEY is required")

    monkeypatch.setattr(routes, "grok_service", FailingGrokStub())
    client = TestClient(app)

    response = client.post("/chat", json=chat_payload())

    assert response.status_code == 503
    assert response.json()["detail"] == "GROK_API_KEY is required"
