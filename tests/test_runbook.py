"""Tests for the runbook documentation."""

from pathlib import Path


def test_runbook_exists() -> None:
    """docs/RUNBOOK.md exists."""
    assert Path("docs/RUNBOOK.md").exists()


def test_runbook_contains_correlation_id() -> None:
    """RUNBOOK.md mentions correlation_id."""
    content = Path("docs/RUNBOOK.md").read_text(encoding="utf-8").lower()

    assert "correlation_id" in content


def test_runbook_contains_health() -> None:
    """RUNBOOK.md mentions health."""
    content = Path("docs/RUNBOOK.md").read_text(encoding="utf-8").lower()

    assert "health" in content


def test_runbook_contains_incident() -> None:
    """RUNBOOK.md mentions incident."""
    content = Path("docs/RUNBOOK.md").read_text(encoding="utf-8").lower()

    assert "incident" in content


def test_runbook_contains_restart() -> None:
    """RUNBOOK.md mentions restart."""
    content = Path("docs/RUNBOOK.md").read_text(encoding="utf-8").lower()

    assert "restart" in content
