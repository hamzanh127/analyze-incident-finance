"""Metrics API routes."""

from fastapi import APIRouter, HTTPException

from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])
metrics_service = MetricsService()


@router.get("")
def get_metrics() -> dict[str, int | float]:
    """Return in-memory service metrics."""
    try:
        return metrics_service.get_metrics()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Metrics retrieval failed") from exc
