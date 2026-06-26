"""Tests for RiskAgent."""

from app.agents.risk_agent import RiskAgent


def test_risk_agent_low_risk(incident, static_grok_factory) -> None:
    """RiskAgent returns a low-risk result."""
    grok = static_grok_factory({"risk_level": "low", "risk_score": 10, "reasons": ["small amount"]})

    result = RiskAgent(grok).analyze(incident)

    assert result["risk_level"] == "low"
    assert result["risk_score"] == 10


def test_risk_agent_medium_risk(incident, static_grok_factory) -> None:
    """RiskAgent returns a medium-risk result."""
    grok = static_grok_factory({"risk_level": "medium", "risk_score": 50, "reasons": ["new beneficiary"]})

    result = RiskAgent(grok).analyze(incident)

    assert result["risk_level"] == "medium"
    assert result["risk_score"] == 50


def test_risk_agent_high_risk(high_risk_incident, static_grok_factory) -> None:
    """RiskAgent returns a high-risk result."""
    grok = static_grok_factory({"risk_level": "high", "risk_score": 95, "reasons": ["large amount"]})

    result = RiskAgent(grok).analyze(high_risk_incident)

    assert result["risk_level"] == "high"
    assert result["risk_score"] == 95


def test_risk_agent_score_does_not_exceed_100(incident, static_grok_factory) -> None:
    """RiskAgent falls back when the score exceeds 100."""
    grok = static_grok_factory({"risk_level": "high", "risk_score": 150, "reasons": ["invalid score"]})

    result = RiskAgent(grok).analyze(incident)

    assert result["risk_score"] <= 100
