"""Incident response schemas."""

from pydantic import BaseModel, Field


class RiskResult(BaseModel):
    """Risk assessment produced by the risk agent."""

    risk_level: str
    risk_score: int = Field(ge=0, le=100)
    factors: list[str] = Field(default_factory=list)


class FraudResult(BaseModel):
    """Fraud assessment produced by the fraud agent."""

    fraud_suspicion: bool
    fraud_score: int = Field(ge=0, le=100)
    indicators: list[str] = Field(default_factory=list)


class ComplianceResult(BaseModel):
    """Compliance assessment produced by the compliance agent."""

    compliance_status: str
    checks: list[str] = Field(default_factory=list)


class MonitoringResult(BaseModel):
    """Monitoring assessment produced by local monitoring checks."""

    latency_ms: float | None = Field(default=None, ge=0)
    token_count: int | None = Field(default=None, ge=0)
    pii_detected: bool = False
    prompt_injection_detected: bool = False
    toxicity_detected: bool = False


class AnalyzeResponse(BaseModel):
    """Response payload returned by incident analysis."""

    correlation_id: str
    risk_level: str
    risk_score: int = Field(ge=0, le=100)
    fraud_suspicion: bool
    fraud_score: int = Field(ge=0, le=100)
    compliance_status: str
    decision: str
    recommendations: list[str] = Field(default_factory=list)
    monitoring: dict[str, object] = Field(default_factory=dict)
    report: dict[str, object] | None = None


class IncidentDecisionResponse(BaseModel):
    """Legacy internal response payload kept for current route compatibility."""

    correlation_id: str
    decision: str
    assessments: dict[str, object]
    latency_ms: float
