"""Tests for structured logs."""

from app.services.logging_service import log_event


def test_log_event_returns_structured_log() -> None:
    """log_event returns all required structured fields."""
    event = log_event(
        correlation_id="FIN-20260626-ABC123",
        event_type="analysis_started",
        message="Analysis started",
        metadata={"agent": "supervisor"},
    )

    assert "timestamp" in event
    assert event["correlation_id"] == "FIN-20260626-ABC123"
    assert event["event_type"] == "analysis_started"
    assert event["message"] == "Analysis started"
    assert event["metadata"] == {"agent": "supervisor"}
