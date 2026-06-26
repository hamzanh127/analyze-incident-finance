"""Observability API routes."""

from typing import Any

from fastapi import APIRouter

from app.monitoring.langsmith_tracing import langsmith_status

router = APIRouter(tags=["observability"])


@router.get("/observability")
def observability() -> dict[str, Any]:
    """Return current LangSmith observability configuration."""
    return langsmith_status()
