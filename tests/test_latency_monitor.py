"""Tests for latency monitoring."""

from time import sleep

from app.monitoring.latency_monitor import LatencyMonitor


def test_latency_monitor_returns_positive_latency() -> None:
    """LatencyMonitor returns a positive elapsed duration."""
    monitor = LatencyMonitor()

    monitor.start_timer()
    sleep(0.001)
    latency_ms = monitor.stop_timer()

    assert latency_ms > 0
