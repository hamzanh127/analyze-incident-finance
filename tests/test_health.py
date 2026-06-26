"""Tests for root and health API endpoints."""

from fastapi.testclient import TestClient

from app.main import app


def test_root_returns_200() -> None:
    """GET / returns HTTP 200."""
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200


def test_health_returns_200() -> None:
    """GET /health returns HTTP 200."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200


def test_health_returns_status_healthy() -> None:
    """GET /health returns healthy status."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.json()["status"] == "healthy"
