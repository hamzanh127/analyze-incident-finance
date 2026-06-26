"""Incident API routes."""

import json
from time import perf_counter
from typing import Any

from fastapi import APIRouter, HTTPException

from app.agents.supervisor_agent import SupervisorAgent
from app.api.metrics import metrics_service
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.schemas.incident_schema import IncidentRequest
from app.schemas.response_schema import AnalyzeResponse
from app.services.grok_service import GrokService, GrokServiceError

router = APIRouter(tags=["analysis"])
supervisor_agent = SupervisorAgent()
grok_service = GrokService()


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


@router.post("/chat", response_model=ChatResponse)
def chat_with_finance_agent(payload: ChatRequest) -> ChatResponse:
    """Answer finance incident questions with Grok using the current analysis context."""
    try:
        answer = grok_service.call_grok(
            system_prompt=_finance_chat_system_prompt(),
            user_prompt=_build_chat_prompt(payload),
        )
        return ChatResponse(message=answer)
    except GrokServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _finance_chat_system_prompt() -> str:
    return (
        "You are the AI Agent Chat for the Finance Incident Multi-Agent project. "
        "Answer only within this project's context: financial incident analysis, Supervisor, Risk Agent, "
        "Fraud Agent, Compliance Agent, Monitoring Agent, LangGraph workflow, LangSmith observability, "
        "metrics, logs, correlation IDs, decisions, recommendations, and analyst next steps. "
        "Use the provided incident, analysis_result, and history. Be concise, practical, and explain the reasoning. "
        "Do not invent backend fields that are not present. If data is missing, say what is missing."
    )


def _build_chat_prompt(payload: ChatRequest) -> str:
    context: dict[str, Any] = {
        "incident": payload.incident or {},
        "analysis_result": payload.analysis_result or {},
        "history": [message.model_dump() for message in payload.history[-10:]],
        "message": payload.message,
    }
    return (
        "Finance incident chat context follows as JSON.\n"
        f"{json.dumps(context, ensure_ascii=False, default=str)}\n\n"
        "Answer the latest user message using this context."
    )
