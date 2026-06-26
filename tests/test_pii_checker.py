"""Tests for PII checker."""

from app.monitoring.pii_checker import detect_pii


def test_pii_checker_detects_email() -> None:
    """detect_pii detects an email address."""
    result = detect_pii("Customer email is client@example.com.")

    assert result["detected"] is True
    assert "email" in result["types"]
    assert result["matches_count"] == 1


def test_pii_checker_detects_simple_credit_card() -> None:
    """detect_pii detects a simple credit card number."""
    result = detect_pii("Card number 4111 1111 1111 1111 was reported.")

    assert result["detected"] is True
    assert "credit_card" in result["types"]


def test_pii_checker_detects_cin() -> None:
    """detect_pii detects a Moroccan CIN."""
    result = detect_pii("My CIN is AB12345.")

    assert result["detected"] is True
    assert "cin" in result["types"]


def test_pii_checker_detects_moroccan_phone() -> None:
    """detect_pii detects a Moroccan phone number."""
    result = detect_pii("Contact me at +212 6 12 34 56 78.")

    assert result["detected"] is True
    assert "phone" in result["types"]


def test_pii_checker_detects_name() -> None:
    """detect_pii detects an explicit name."""
    result = detect_pii("nom: Hamza Nachat")

    assert result["detected"] is True
    assert "name" in result["types"]
    assert result["matches_count"] == 1
