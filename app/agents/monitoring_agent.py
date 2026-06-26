"""Monitoring agent for multi-agent execution tracking."""

from typing import Any

from app.monitoring.langsmith_tracing import monitoring_langsmith_payload
from app.monitoring.monitoring_service import MonitoringService
from app.schemas.incident_schema import IncidentRequest

OBSERVABILITY_FLAGS: dict[str, bool] = {
    "logs_enabled": True,
    "metrics_enabled": True,
    "correlation_id_enabled": True,
    "toxicity_check_enabled": True,
    "prompt_injection_check_enabled": True,
    "pii_check_enabled": True,
    "grok_safety_review_enabled": True,
}


class MonitoringAgent:
    """Track execution state for the multi-agent analysis workflow."""

    def __init__(self, monitoring_service: MonitoringService | None = None) -> None:
        """Initialize the monitoring agent."""
        self._monitoring_service = monitoring_service or MonitoringService()

    def start(self, correlation_id: str) -> dict[str, Any]:
        """Return the initial monitoring state for an analysis execution."""
        return self._build_payload(
            correlation_id=correlation_id,
            status="processed",
            execution_time_ms=0.0,
        )

    def finish(
        self,
        correlation_id: str,
        status: str,
        execution_time_ms: float,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return the final monitoring state for an analysis execution."""
        normalized_status = status if status in {"processed", "failed"} else "failed"
        payload = self._build_payload(
            correlation_id=correlation_id,
            status=normalized_status,
            execution_time_ms=execution_time_ms,
        )
        if extra is not None:
            payload["extra"] = extra
        return payload

    def analyze(self, incident: IncidentRequest) -> dict[str, bool]:
        """Return local monitoring check results for current workflow compatibility."""
        return self._monitoring_service.evaluate(incident.description)

    def analyze_full(self, text: str) -> dict[str, Any]:
        """Run the full hybrid analysis and return Static Checks, Grok Review and Final Decision."""
        result = self._monitoring_service.analyze_text(text)
        return {
            "static_checks": result.get("static_checks", {}),
            "grok_safety_review": result.get("grok_safety_review", {}),
            "final_decision": result.get("final_decision", {}),
            "safe": result.get("safe", True),
            "metrics": result.get("metrics", {}),
        }

    def _build_payload(
        self,
        correlation_id: str,
        status: str,
        execution_time_ms: float,
    ) -> dict[str, Any]:
        return {
            "correlation_id": correlation_id,
            "status": status,
            "execution_time_ms": execution_time_ms,
            "observability": dict(OBSERVABILITY_FLAGS),
            "langsmith": monitoring_langsmith_payload(),
        }
