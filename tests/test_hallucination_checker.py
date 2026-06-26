"""Tests for hallucination checker."""

from app.monitoring.hallucination_checker import check_hallucination


def test_hallucination_checker_returns_known_risk_level() -> None:
    """check_hallucination returns low, medium, or high."""
    result = check_hallucination("This result is guaranteed.")

    assert result["risk_level"] in {"low", "medium", "high"}
