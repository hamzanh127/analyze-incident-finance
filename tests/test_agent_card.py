"""Tests for the agent card metadata."""

import json
from pathlib import Path


def test_agent_card_exists() -> None:
    """agent_card.json exists."""
    assert Path("agent_card.json").exists()


def test_agent_card_contains_required_fields() -> None:
    """agent_card.json contains required top-level fields."""
    agent_card = json.loads(Path("agent_card.json").read_text(encoding="utf-8"))

    required_fields = {"name", "version", "owner", "agents", "inputs", "outputs", "monitoring"}

    assert required_fields.issubset(agent_card)
