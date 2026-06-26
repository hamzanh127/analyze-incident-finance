"""Tests for token monitoring."""

from app.monitoring.token_monitor import estimate_tokens


def test_token_monitor_returns_tokens_greater_than_zero() -> None:
    """estimate_tokens returns a positive token estimate."""
    result = estimate_tokens("Analyze this financial incident")

    assert result["estimated_tokens"] > 0
