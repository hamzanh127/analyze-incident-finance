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


def test_toxicity_checker_returns_unsafe_for_french_toxic_text() -> None:
    """check_toxicity returns unsafe for French toxic text."""
    result = check_toxicity("C'est une putain de transaction.")

    assert result["status"] == "unsafe"
    assert "putain" in result["matched_terms"]
