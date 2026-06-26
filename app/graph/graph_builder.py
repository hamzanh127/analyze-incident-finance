"""LangGraph builder for the finance incident workflow."""

from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    ai_safety_node,
    compliance_node,
    decision_node,
    fraud_node,
    monitoring_node,
    report_node,
    risk_node,
)
from app.graph.state import FinanceIncidentState


def build_finance_incident_graph():
    """Build and compile the finance incident LangGraph."""
    graph = StateGraph(FinanceIncidentState)
    graph.add_node("risk_node", risk_node)
    graph.add_node("fraud_node", fraud_node)
    graph.add_node("compliance_node", compliance_node)
    graph.add_node("ai_safety_node", ai_safety_node)
    graph.add_node("decision_node", decision_node)
    graph.add_node("monitoring_node", monitoring_node)
    graph.add_node("report_node", report_node)

    graph.add_edge(START, "risk_node")
    graph.add_edge("risk_node", "fraud_node")
    graph.add_edge("fraud_node", "compliance_node")
    graph.add_edge("compliance_node", "ai_safety_node")
    graph.add_edge("ai_safety_node", "decision_node")
    graph.add_edge("decision_node", "monitoring_node")
    graph.add_edge("monitoring_node", "report_node")
    graph.add_edge("report_node", END)
    return graph.compile()


compiled_finance_graph = build_finance_incident_graph()
