"""LangSmith tracing helpers for the LangGraph workflow."""

from collections.abc import Callable
from datetime import UTC, datetime
from time import perf_counter
from typing import Any, TypeVar

from app.config import Settings, get_settings

try:
    from langsmith import traceable
except ImportError:  # pragma: no cover - dependency is declared, fallback keeps local imports safe.
    traceable = None

LANGSMITH_RUN_NAME = "finance_incident_analysis"
LANGSMITH_PROJECT = "finance-incident-multi-agent"

T = TypeVar("T")


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp for trace metadata."""
    return datetime.now(UTC).isoformat()


def langsmith_status(settings: Settings | None = None) -> dict[str, Any]:
    """Return public LangSmith observability status."""
    active_settings = settings or get_settings()
    return {
        "langsmith_enabled": active_settings.langsmith_enabled,
        "project": active_settings.langsmith_project,
        "tracing": active_settings.langsmith_enabled,
        "environment": active_settings.environment,
        "version": active_settings.app_version,
    }


def monitoring_langsmith_payload(settings: Settings | None = None) -> dict[str, Any]:
    """Return the LangSmith block embedded in MonitoringAgent output."""
    active_settings = settings or get_settings()
    if not active_settings.langsmith_enabled:
        return {"enabled": False}
    return {
        "enabled": True,
        "project": active_settings.langsmith_project,
        "trace_available": True,
    }


def build_trace_metadata(
    state: dict[str, Any],
    *,
    execution_time_ms: float | None = None,
) -> dict[str, Any]:
    """Build normalized LangSmith metadata from workflow state."""
    settings = get_settings()
    incident = state.get("incident")
    risk_result = state.get("risk_result", {})
    metadata = {
        "correlation_id": state.get("correlation_id", ""),
        "request_id": state.get("request_id", state.get("correlation_id", "")),
        "incident_type": _incident_value(incident, "incident_type", ""),
        "amount": _incident_value(incident, "amount", 0),
        "risk_level": risk_result.get("risk_level", ""),
        "decision": state.get("decision", ""),
        "execution_time": execution_time_ms if execution_time_ms is not None else state.get("execution_time_ms", 0),
        "environment": settings.environment,
        "application_version": settings.app_version,
        "version": settings.app_version,
        "timestamp": state.get("timestamp", utc_timestamp()),
    }
    return metadata


def graph_invoke_config(state: dict[str, Any]) -> dict[str, Any]:
    """Return LangGraph invoke config carrying the LangSmith run name and metadata."""
    return {
        "run_name": LANGSMITH_RUN_NAME,
        "metadata": build_trace_metadata(state),
        "tags": ["finance_incident", "multi_agent", "langgraph"],
    }


def trace_step(name: str, state: dict[str, Any], func: Callable[[], T]) -> T:
    """Trace a workflow step as a distinct LangSmith run when tracing is enabled."""
    settings = get_settings()
    if not settings.langsmith_enabled or traceable is None:
        return func()

    start = perf_counter()

    @traceable(name=name, run_type="chain", metadata=build_trace_metadata(state))
    def _run() -> T:
        return func()

    result = _run()
    state["execution_time_ms"] = round((perf_counter() - start) * 1000, 3)
    return result


def _incident_value(incident: Any, field_name: str, default: Any) -> Any:
    if isinstance(incident, dict):
        return incident.get(field_name, default)
    return getattr(incident, field_name, default)
