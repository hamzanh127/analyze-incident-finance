"""Risk analysis agent."""

from typing import Any

from app.schemas.incident_schema import IncidentRequest
from app.services.grok_service import GrokParsingError, GrokService, GrokServiceError

ALLOWED_RISK_LEVELS = {"low", "medium", "high"}
FALLBACK_RISK_RESULT: dict[str, Any] = {
    "risk_level": "medium",
    "risk_score": 50,
    "reasons": ["Fallback risk analysis due to Grok response error"],
}


class RiskAgent:
    """AI agent specialized in financial risk analysis."""

    def __init__(self, grok_service: GrokService | None = None) -> None:
        """Initialize the risk agent with an injectable Grok service."""
        self._grok_service = grok_service or GrokService()

    def analyze(self, incident: IncidentRequest) -> dict[str, Any]:
        """Analyze a financial incident risk profile with Grok."""
        try:
            response = self._grok_service.call_grok_json(
                system_prompt=self._build_system_prompt(),
                user_prompt=self._build_user_prompt(incident),
            )
            return self._validate_response(response)
        except (GrokServiceError, GrokParsingError, ValueError, TypeError):
            return dict(FALLBACK_RISK_RESULT)

    def _build_system_prompt(self) -> str:
        return (
            "You are an expert in financial risk management.\n"
            "Your mission is to analyze the risk level of a financial incident.\n"
            "Return strictly and only a JSON object with this schema:\n"
            '{"risk_level":"low|medium|high","risk_score":0,"reasons":[]}\n'
            "Do not add any text outside the JSON object."
        )

    def _build_user_prompt(self, incident: IncidentRequest) -> str:
        return (
            "Analyze this financial incident:\n"
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
        risk_level = response.get("risk_level", FALLBACK_RISK_RESULT["risk_level"])
        if risk_level not in ALLOWED_RISK_LEVELS:
            risk_level = FALLBACK_RISK_RESULT["risk_level"]

        risk_score = response.get("risk_score", FALLBACK_RISK_RESULT["risk_score"])
        if not isinstance(risk_score, int) or not 0 <= risk_score <= 100:
            risk_score = FALLBACK_RISK_RESULT["risk_score"]

        reasons = response.get("reasons", [])
        if not isinstance(reasons, list):
            reasons = []

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "reasons": reasons,
        }
