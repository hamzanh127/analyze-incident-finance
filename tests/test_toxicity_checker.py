"""Tests for toxicity checker."""

from app.monitoring.toxicity_checker import check_toxicity


def test_toxicity_checker_returns_safe_for_normal_text() -> None:
    """check_toxicity returns safe for normal text."""
    result = check_toxicity("This transaction requires a standard review.")

    assert result["status"] == "safe"


def test_toxicity_checker_returns_unsafe_for_toxic_text() -> None:
    """check_toxicity returns unsafe for toxic text."""
    result = check_toxicity("This message contains a threat.")

    assert result["status"] == "unsafe"
