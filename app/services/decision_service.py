"""Incident decision service."""

from app.agents.supervisor_agent import SupervisorAgent
from app.monitoring.latency_monitor import LatencyMonitor
from app.schemas.incident_schema import IncidentRequest
from app.schemas.response_schema import IncidentDecisionResponse
from app.services.correlation_service import CorrelationService
from app.services.metrics_service import MetricsService


def decide_final_action(risk_level: str, fraud_suspicion: bool, compliance_status: str) -> str:
    """Return the final deterministic action for an analyzed incident."""
    if compliance_status == "escalation_required":
        return "blocked"
    if risk_level == "high" and fraud_suspicion is True:
        return "blocked"
    if compliance_status == "review_required":
        return "manual_review"
    if risk_level == "low" and fraud_suspicion is False:
        return "approved"
    return "manual_review"


class DecisionService:
    """Coordinate incident analysis and decision creation."""

    def __init__(
        self,
        supervisor_agent: SupervisorAgent | None = None,
        correlation_service: CorrelationService | None = None,
        latency_monitor: LatencyMonitor | None = None,
        metrics_service: MetricsService | None = None,
    ) -> None:
        """Initialize the decision service dependencies."""
        self._supervisor_agent = supervisor_agent or SupervisorAgent()
        self._correlation_service = correlation_service or CorrelationService()
        self._latency_monitor = latency_monitor or LatencyMonitor()
        self._metrics_service = metrics_service or MetricsService()

    def analyze(self, incident: IncidentRequest) -> IncidentDecisionResponse:
        """Analyze an incident and return a simple decision response."""
        start_time = self._latency_monitor.start()
        assessments = self._supervisor_agent.analyze(incident)
        risk_level = str(assessments.get("risk", "medium"))
        fraud_suspicion = assessments.get("fraud") == "suspected"
        compliance_status = str(assessments.get("compliance", "review_required"))
        decision = decide_final_action(risk_level, fraud_suspicion, compliance_status)
        latency_ms = self._latency_monitor.elapsed_ms(start_time)
        self._metrics_service.record_request(latency_ms, risk_level, decision)
        return IncidentDecisionResponse(
            correlation_id=self._correlation_service.new_correlation_id(),
            decision=decision,
            assessments=assessments,
            latency_ms=latency_ms,
        )
