"""Tests for ComplianceAgent."""

from app.agents.compliance_agent import ComplianceAgent


def test_compliance_agent_compliant(incident, static_grok_factory) -> None:
    """ComplianceAgent returns compliant."""
    grok = static_grok_factory(
        {"compliance_status": "compliant", "required_action": "none", "reasons": []}
    )

    result = ComplianceAgent(grok).analyze(incident, {}, {})

    assert result["compliance_status"] == "compliant"
    assert result["required_action"] == "none"


def test_compliance_agent_review_required(incident, static_grok_factory) -> None:
    """ComplianceAgent returns review_required."""
    grok = static_grok_factory(
        {
            "compliance_status": "review_required",
            "required_action": "manual_validation",
            "reasons": ["manual review needed"],
        }
    )

    result = ComplianceAgent(grok).analyze(incident, {}, {})

    assert result["compliance_status"] == "review_required"
    assert result["required_action"] == "manual_validation"


def test_compliance_agent_escalation_required(incident, static_grok_factory) -> None:
    """ComplianceAgent returns escalation_required."""
    grok = static_grok_factory(
        {
            "compliance_status": "escalation_required",
            "required_action": "escalate_to_compliance_team",
            "reasons": ["AML escalation"],
        }
    )

    result = ComplianceAgent(grok).analyze(incident, {}, {})

    assert result["compliance_status"] == "escalation_required"
    assert result["required_action"] == "escalate_to_compliance_team"
