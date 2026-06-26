"""Incident API routes."""

from time import perf_counter

from fastapi import APIRouter, HTTPException

from app.agents.supervisor_agent import SupervisorAgent
from app.api.metrics import metrics_service
from app.schemas.incident_schema import IncidentRequest
from app.schemas.response_schema import AnalyzeResponse

router = APIRouter(tags=["analysis"])
supervisor_agent = SupervisorAgent()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_incident(payload: IncidentRequest) -> AnalyzeResponse:
    """Analyze a finance incident with the multi-agent workflow."""
    start_time = perf_counter()
    try:
        result = supervisor_agent.analyze(payload)
        latency_ms = round((perf_counter() - start_time) * 1000, 3)
        metrics_service.record_request(
            latency_ms=latency_ms,
            risk_level=str(result.get("risk_level")),
            decision=str(result.get("decision")),
        )
        return AnalyzeResponse.model_validate(result)
    except HTTPException:
        metrics_service.record_error()
        raise
    except Exception as exc:
        metrics_service.record_error()
        raise HTTPException(status_code=500, detail="Incident analysis failed") from exc
