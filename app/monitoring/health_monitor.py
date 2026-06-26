"""Application health monitor."""


def check_health() -> dict[str, object]:
    """Return the deterministic health state of core agents."""
    agents = {
        "supervisor_agent": "ok",
        "risk_agent": "ok",
        "fraud_agent": "ok",
        "compliance_agent": "ok",
        "monitoring_agent": "ok",
    }
    return {
        "status": "healthy",
        "agents": agents,
    }


class HealthMonitor:
    """Report local application health."""

    def status(self) -> dict[str, object]:
        """Return a minimal health status payload."""
        return check_health()
