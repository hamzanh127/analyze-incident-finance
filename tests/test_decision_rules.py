"""Tests for decision rules."""

from app.services.decision_service import decide_final_action


def test_decide_final_action_approved() -> None:
    """Low risk without fraud is approved."""
    assert decide_final_action("low", False, "compliant") == "approved"


def test_decide_final_action_manual_review_for_review_required() -> None:
    """Compliance review required returns manual_review."""
    assert decide_final_action("medium", False, "review_required") == "manual_review"


def test_decide_final_action_blocked_for_escalation_required() -> None:
    """Compliance escalation returns blocked."""
    assert decide_final_action("low", False, "escalation_required") == "blocked"


def test_decide_final_action_blocked_for_high_risk_fraud() -> None:
    """High risk with fraud suspicion returns blocked."""
    assert decide_final_action("high", True, "compliant") == "blocked"
