"""Shared pytest fixtures."""

import os
from collections.abc import Iterator
from typing import Any

import pytest

os.environ["LANGSMITH_TRACING"] = "false"
os.environ["LANGSMITH_API_KEY"] = ""

from app.schemas.incident_schema import IncidentRequest


class StaticGrokService:
    """Test double returning a static JSON payload."""

    def __init__(self, response: dict[str, Any]) -> None:
        """Initialize the fake Grok service."""
        self.response = response

    def call_grok_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Return the configured response."""
        return self.response


@pytest.fixture
def incident() -> IncidentRequest:
    """Return a standard finance incident fixture."""
    return IncidentRequest(
        customer_id="cust_123",
        incident_type="wire_transfer",
        amount=1_500.0,
        currency="USD",
        country="US",
        device="mobile",
        beneficiary_status="new",
        description="Transfer to a new beneficiary requires review.",
    )


@pytest.fixture
def high_risk_incident() -> IncidentRequest:
    """Return a high-risk finance incident fixture."""
    return IncidentRequest(
        customer_id="cust_999",
        incident_type="international_transfer",
        amount=25_000.0,
        currency="USD",
        country="US",
        device="unknown_device",
        beneficiary_status="new",
        description="Large international transfer to a new beneficiary.",
    )


@pytest.fixture
def static_grok_factory() -> Iterator[type[StaticGrokService]]:
    """Return the static Grok service test double class."""
    yield StaticGrokService
