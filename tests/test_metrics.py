"""Tests for MetricsService."""

from app.services.metrics_service import MetricsService


def test_metrics_service_increments_request_counters() -> None:
    """MetricsService records requests and derived counters."""
    metrics = MetricsService()

    metrics.record_request(latency_ms=100.0, risk_level="high", decision="blocked")
    metrics.record_request(latency_ms=200.0, risk_level="low", decision="manual_review")

    snapshot = metrics.get_metrics()
    assert snapshot["total_requests"] == 2
    assert snapshot["total_high_risk"] == 1
    assert snapshot["total_blocked"] == 1
    assert snapshot["total_manual_review"] == 1
    assert snapshot["average_latency_ms"] == 150.0


def test_metrics_service_increments_errors() -> None:
    """MetricsService records errors."""
    metrics = MetricsService()

    metrics.record_error()

    assert metrics.get_metrics()["total_errors"] == 1
