"""Health check API routes."""

from fastapi import APIRouter, HTTPException

from app.monitoring.health_monitor import check_health

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict[str, object]:
    """Return the application health status."""
    try:
        health = check_health()
        return {
            "service": "finance-incident-multi-agent",
            **health,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Health check failed") from exc
