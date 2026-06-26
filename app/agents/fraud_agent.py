"""Fraud analysis agent."""

from typing import Any

from app.schemas.incident_schema import IncidentRequest
from app.services.grok_service import GrokParsingError, GrokService, GrokServiceError

FALLBACK_FRAUD_RESULT: dict[str, Any] = {
    "fraud_suspicion": False,
    "fraud_score": 30,
    "signals": ["Fallback fraud analysis due to Grok response error"],
}


class FraudAgent:
    """AI agent specialized in financial fraud detection."""

    def __init__(self, grok_service: GrokService | None = None) -> None:
        """Initialize the fraud agent with an injectable Grok service."""
        self._grok_service = grok_service or GrokService()

    def analyze(self, incident: IncidentRequest) -> dict[str, Any]:
        """Analyze a financial incident for fraud signals with Grok."""
        try:
            response = self._grok_service.call_grok_json(
                system_prompt=self._build_system_prompt(),
                user_prompt=self._build_user_prompt(incident),
            )
            return self._validate_response(response)
        except (GrokServiceError, GrokParsingError, ValueError, TypeError):
            return dict(FALLBACK_FRAUD_RESULT)

    def _build_system_prompt(self) -> str:
        return (
            "You are an expert in banking fraud and suspicious transactions.\n"
            "Your mission is to detect fraud signals in a financial incident.\n"
            "Return strictly and only a JSON object with this schema:\n"
            '{"fraud_suspicion":false,"fraud_score":0,"signals":[]}\n'
            "Do not add any text outside the JSON object."
        )

    def _build_user_prompt(self, incident: IncidentRequest) -> str:
        return (
            "Analyze this complete financial incident for fraud:\n"
            f"customer_id: {incident.customer_id}\n"
            f"incident_type: {incident.incident_type}\n"
            f"amount: {incident.amount}\n"
            f"currency: {incident.currency}\n"
            f"country: {incident.country}\n"
            f"device: {incident.device}\n"
            f"beneficiary_status: {incident.beneficiary_status}\n"
            f"description: {incident.description}"
        )

    def _validate_response(self, response: dict[str, Any]) -> dict[str, Any]:
        fraud_suspicion = response.get(
            "fraud_suspicion",
            FALLBACK_FRAUD_RESULT["fraud_suspicion"],
        )
        if not isinstance(fraud_suspicion, bool):
            fraud_suspicion = FALLBACK_FRAUD_RESULT["fraud_suspicion"]

        fraud_score = response.get("fraud_score", FALLBACK_FRAUD_RESULT["fraud_score"])
        if not isinstance(fraud_score, int) or not 0 <= fraud_score <= 100:
            fraud_score = FALLBACK_FRAUD_RESULT["fraud_score"]

        signals = response.get("signals", [])
        if not isinstance(signals, list):
            signals = []

        return {
            "fraud_suspicion": fraud_suspicion,
            "fraud_score": fraud_score,
            "signals": signals,
        }
