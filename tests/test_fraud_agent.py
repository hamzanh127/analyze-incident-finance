"""Tests for FraudAgent."""

from app.agents.fraud_agent import FraudAgent


def test_fraud_agent_detects_fraud(incident, static_grok_factory) -> None:
    """FraudAgent detects suspected fraud."""
    grok = static_grok_factory(
        {"fraud_suspicion": True, "fraud_score": 90, "signals": ["unauthorized transfer"]}
    )

    result = FraudAgent(grok).analyze(incident)

    assert result["fraud_suspicion"] is True
    assert result["fraud_score"] == 90


def test_fraud_agent_normal_transaction(incident, static_grok_factory) -> None:
    """FraudAgent handles a normal transaction."""
    grok = static_grok_factory({"fraud_suspicion": False, "fraud_score": 5, "signals": []})

    result = FraudAgent(grok).analyze(incident)

    assert result["fraud_suspicion"] is False
    assert result["fraud_score"] == 5


def test_fraud_agent_signals_are_filled(incident, static_grok_factory) -> None:
    """FraudAgent returns fraud signals."""
    grok = static_grok_factory({"fraud_suspicion": True, "fraud_score": 70, "signals": ["new device"]})

    result = FraudAgent(grok).analyze(incident)

    assert result["signals"] == ["new device"]
