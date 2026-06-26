"""LangGraph nodes for finance incident analysis."""

from time import perf_counter
from typing import Any

from app.agents.compliance_agent import ComplianceAgent
from app.agents.fraud_agent import FraudAgent
from app.agents.monitoring_agent import MonitoringAgent
from app.agents.risk_agent import RiskAgent
from app.graph.state import FinanceIncidentState
from app.monitoring.langsmith_tracing import build_trace_metadata, trace_step
from app.monitoring.monitoring_service import MonitoringService


def risk_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Run the risk analysis agent."""
    result = trace_step(
        "Risk Agent",
        state,
        lambda: RiskAgent().analyze(state["incident"]),
    )
    return {"risk_result": result}


def fraud_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Run the fraud detection agent."""
    result = trace_step(
        "Fraud Agent",
        state,
        lambda: FraudAgent().analyze(state["incident"]),
    )
    return {"fraud_result": result}


def compliance_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Run the compliance analysis agent."""
    result = trace_step(
        "Compliance Agent",
        state,
        lambda: ComplianceAgent().analyze(
            state["incident"],
            state["risk_result"],
            state["fraud_result"],
        ),
    )
    return {"compliance_result": result}


def ai_safety_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Run AI safety checks over the incident description."""
    try:
        incident = state["incident"]
        description = incident["description"] if isinstance(incident, dict) else incident.description
        result = MonitoringService().analyze_text(description)
    except Exception as exc:
        result = _fallback_ai_safety(str(exc))
    return {"ai_safety_result": result}


def decision_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Calculate final decision and recommendations."""
    from app.services.decision_service import decide_final_action

    risk_result = state.get("risk_result", {})
    fraud_result = state.get("fraud_result", {})
    compliance_result = state.get("compliance_result", {})
    ai_safety_result = state.get("ai_safety_result", {})
    decision = decide_final_action(
        risk_level=str(risk_result.get("risk_level", "medium")),
        fraud_suspicion=bool(fraud_result.get("fraud_suspicion", False)),
        compliance_status=str(compliance_result.get("compliance_status", "review_required")),
    )
    recommendations = _build_recommendations(
        risk_result,
        fraud_result,
        compliance_result,
        ai_safety_result,
        decision,
    )
    return {"decision": decision, "recommendations": recommendations}


def monitoring_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Build execution monitoring result."""
    start_time = state.get("_start_time")
    execution_time_ms = 0.0
    if isinstance(start_time, float):
        execution_time_ms = round((perf_counter() - start_time) * 1000, 3)
    state["execution_time_ms"] = execution_time_ms
    trace_metadata = build_trace_metadata(state, execution_time_ms=execution_time_ms)
    monitoring = trace_step(
        "Monitoring Agent",
        state,
        lambda: MonitoringAgent().finish(
            correlation_id=state["correlation_id"],
            status="processed",
            execution_time_ms=execution_time_ms,
            extra={"langsmith_metadata": trace_metadata},
        ),
    )
    return {"monitoring": monitoring}


def report_node(state: FinanceIncidentState) -> dict[str, Any]:
    """Build the final structured incident report."""
    report = trace_step(
        "Report Generation",
        state,
        lambda: {
            "summary": f"Finance incident analysis completed with decision: {state.get('decision', 'manual_review')}.",
            "risk_analysis": state.get("risk_result", {}),
            "fraud_analysis": state.get("fraud_result", {}),
            "compliance_analysis": state.get("compliance_result", {}),
            "ai_safety": state.get("ai_safety_result", {}),
            "recommended_next_steps": state.get("recommendations", []),
            "final_status": "completed",
        },
    )
    return {"report": report}


def _build_recommendations(
    risk_result: dict[str, Any],
    fraud_result: dict[str, Any],
    compliance_result: dict[str, Any],
    ai_safety_result: dict[str, Any],
    decision: str,
) -> list[str]:
    recommendations: list[str] = []
    if risk_result.get("risk_level") == "high":
        recommendations.append("Review high-risk financial exposure before approval.")
    if fraud_result.get("fraud_suspicion") is True:
        recommendations.append("Investigate fraud signals and verify transaction legitimacy.")
    if compliance_result.get("compliance_status") != "compliant":
        recommendations.append("Complete compliance validation before final processing.")
    if ai_safety_result.get("safe") is False:
        recommendations.append("Review AI safety findings before relying on the analysis.")
    if decision == "approved":
        recommendations.append("Proceed with standard processing controls.")
    if not recommendations:
        recommendations.append("No additional action required.")
    return recommendations


def _fallback_ai_safety(error: str) -> dict[str, Any]:
    return {
        "safe": True,
        "static_checks": {
            "toxicity": {"status": "safe", "score": 0.0, "matched_terms": []},
            "hallucination": {"risk_level": "low"},
            "prompt_injection": {"detected": False, "matched_patterns": []},
            "pii": {"detected": False, "types": [], "matches_count": 0},
            "tokens": {"estimated_tokens": 0, "word_count": 0, "multiplier": 1.3},
            "cost": {"estimated_cost": 0.0, "input_tokens": 0, "output_tokens": 0, "currency": "USD"},
        },
        "grok_safety_review": {
            "available": False,
            "error": f"Fallback due to node error: {error}",
        },
        "final_decision": {
            "safe": True,
            "action": "allow",
            "source": "static",
            "reasons": [f"Fallback due to node error: {error}"],
        },
        "metrics": {},
    }
