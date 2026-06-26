"""Tests for PII checker."""

from app.monitoring.pii_checker import detect_pii


def test_pii_checker_detects_email() -> None:
    """detect_pii detects an email address."""
    result = detect_pii("Customer email is client@example.com.")

    assert result["detected"] is True
    assert "email" in result["types"]


def test_pii_checker_detects_simple_credit_card() -> None:
    """detect_pii detects a simple credit card number."""
    result = detect_pii("Card number 4111 1111 1111 1111 was reported.")

    assert result["detected"] is True
    assert "credit_card" in result["types"]
