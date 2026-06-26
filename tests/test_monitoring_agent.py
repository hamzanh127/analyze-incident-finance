"""Tests for MonitoringAgent."""

from app.agents.monitoring_agent import MonitoringAgent


def test_monitoring_agent_start_returns_correlation_id() -> None:
    """MonitoringAgent.start returns the correlation id."""
    result = MonitoringAgent().start("FIN-20260626-ABC123")

    assert result["correlation_id"] == "FIN-20260626-ABC123"


def test_monitoring_agent_finish_returns_execution_time_ms() -> None:
    """MonitoringAgent.finish returns execution time."""
    result = MonitoringAgent().finish("FIN-20260626-ABC123", "processed", 120.5)

    assert result["execution_time_ms"] == 120.5


def test_monitoring_agent_observability_contains_correlation_id_enabled() -> None:
    """MonitoringAgent observability includes correlation tracking."""
    result = MonitoringAgent().start("FIN-20260626-ABC123")

    assert result["observability"]["correlation_id_enabled"] is True
