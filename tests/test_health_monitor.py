"""Tests for health monitoring."""

from app.monitoring.health_monitor import check_health


def test_health_monitor_returns_healthy_status() -> None:
    """check_health returns healthy service status."""
    result = check_health()

    assert result["status"] == "healthy"
