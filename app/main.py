"""FastAPI application entrypoint."""

from fastapi import APIRouter, FastAPI

from app.api.health import router as health_router
from app.api.metrics import router as metrics_router
from app.api.observability import router as observability_router
from app.api.routes import router as incident_router

SERVICE_NAME = "finance-incident-multi-agent"
SERVICE_VERSION = "1.8.0"

root_router = APIRouter(tags=["root"])


@root_router.get("/")
def root() -> dict[str, str]:
    """Return the service status."""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "running",
    }


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=SERVICE_NAME,
        version=SERVICE_VERSION,
    )
    
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(root_router)
    app.include_router(health_router)
    app.include_router(metrics_router)
    app.include_router(observability_router)
    app.include_router(incident_router)
    return app


app = create_app()
