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
    graph.add_node("Risk Agent", risk_node)
    graph.add_node("Fraud Agent", fraud_node)
    graph.add_node("Compliance Agent", compliance_node)
    graph.add_node("AI Safety Checks", ai_safety_node)
    graph.add_node("Decision Engine", decision_node)
    graph.add_node("Monitoring Agent", monitoring_node)
    graph.add_node("Report Generation", report_node)

    graph.add_edge(START, "Risk Agent")
    graph.add_edge("Risk Agent", "Fraud Agent")
    graph.add_edge("Fraud Agent", "Compliance Agent")
    graph.add_edge("Compliance Agent", "AI Safety Checks")
    graph.add_edge("AI Safety Checks", "Decision Engine")
    graph.add_edge("Decision Engine", "Monitoring Agent")
    graph.add_edge("Monitoring Agent", "Report Generation")
    graph.add_edge("Report Generation", END)
    return graph.compile()


compiled_finance_graph = build_finance_incident_graph()
