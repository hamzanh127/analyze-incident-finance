"""Tests for invalid analyze API payloads."""

from fastapi.testclient import TestClient

from app.main import app
from tests.test_analyze_api import valid_payload


def test_analyze_with_negative_amount_returns_422() -> None:
    """POST /analyze with negative amount returns HTTP 422."""
    client = TestClient(app)
    payload = valid_payload()
    payload["amount"] = -1

    response = client.post("/analyze", json=payload)

    assert response.status_code == 422


def test_analyze_without_description_returns_422() -> None:
    """POST /analyze without description returns HTTP 422."""
    client = TestClient(app)
    payload = valid_payload()
    payload.pop("description")

    response = client.post("/analyze", json=payload)

    assert response.status_code == 422
