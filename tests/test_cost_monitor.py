"""Tests for cost monitoring."""

from app.monitoring.cost_monitor import estimate_cost


def test_cost_monitor_returns_non_negative_cost() -> None:
    """estimate_cost returns a non-negative cost."""
    result = estimate_cost(input_tokens=100, output_tokens=50)

    assert result["estimated_cost"] >= 0
