"""Compliance analysis agent."""

from typing import Any

from app.schemas.incident_schema import IncidentRequest
from app.services.grok_service import GrokParsingError, GrokService, GrokServiceError

ALLOWED_COMPLIANCE_STATUSES = {"compliant", "review_required", "escalation_required"}
ALLOWED_REQUIRED_ACTIONS = {"none", "manual_validation", "escalate_to_compliance_team"}
FALLBACK_COMPLIANCE_RESULT: dict[str, Any] = {
    "compliance_status": "review_required",
    "required_action": "manual_validation",
    "reasons": ["Fallback compliance analysis due to Grok response error"],
}


class ComplianceAgent:
    """AI agent specialized in banking compliance analysis."""

    def __init__(self, grok_service: GrokService | None = None) -> None:
        """Initialize the compliance agent with an injectable Grok service."""
        self._grok_service = grok_service or GrokService()

    def analyze(
        self,
        incident: IncidentRequest,
        risk_result: dict[str, Any],
        fraud_result: dict[str, Any],
    ) -> dict[str, Any]:
        """Analyze compliance requirements for a financial incident with Grok."""
        try:
            response = self._grok_service.call_grok_json(
                system_prompt=self._build_system_prompt(),
                user_prompt=self._build_user_prompt(incident, risk_result, fraud_result),
            )
            return self._validate_response(response)
        except (GrokServiceError, GrokParsingError, ValueError, TypeError):
            return dict(FALLBACK_COMPLIANCE_RESULT)

    def _build_system_prompt(self) -> str:
        return (
            "You are an expert in banking compliance, AML, KYC, and financial governance.\n"
            "Your mission is to determine whether a financial incident requires human review "
            "or compliance escalation.\n"
            "Return strictly and only a JSON object with this schema:\n"
            '{"compliance_status":"compliant|review_required|escalation_required",'
            '"required_action":"none|manual_validation|escalate_to_compliance_team",'
            '"reasons":[]}\n'
            "Do not add any text outside the JSON object."
        )

    def _build_user_prompt(
        self,
        incident: IncidentRequest,
        risk_result: dict[str, Any],
        fraud_result: dict[str, Any],
    ) -> str:
        return (
            "Analyze this complete financial incident for compliance:\n"
            f"customer_id: {incident.customer_id}\n"
            f"incident_type: {incident.incident_type}\n"
            f"amount: {incident.amount}\n"
            f"currency: {incident.currency}\n"
            f"country: {incident.country}\n"
            f"device: {incident.device}\n"
            f"beneficiary_status: {incident.beneficiary_status}\n"
            f"description: {incident.description}\n"
            f"risk_result: {risk_result}\n"
            f"fraud_result: {fraud_result}"
        )

    def _validate_response(self, response: dict[str, Any]) -> dict[str, Any]:
        compliance_status = response.get(
            "compliance_status",
            FALLBACK_COMPLIANCE_RESULT["compliance_status"],
        )
        if compliance_status not in ALLOWED_COMPLIANCE_STATUSES:
            compliance_status = FALLBACK_COMPLIANCE_RESULT["compliance_status"]

        required_action = response.get(
            "required_action",
            FALLBACK_COMPLIANCE_RESULT["required_action"],
        )
        if required_action not in ALLOWED_REQUIRED_ACTIONS:
            required_action = FALLBACK_COMPLIANCE_RESULT["required_action"]

        reasons = response.get("reasons", [])
        if not isinstance(reasons, list):
            reasons = []

        return {
            "compliance_status": compliance_status,
            "required_action": required_action,
            "reasons": reasons,
        }
