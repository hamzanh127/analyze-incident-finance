"""Application metrics service."""


class MetricsService:
    """Keep deterministic in-memory metrics for API requests."""

    def __init__(self) -> None:
        """Initialize all metrics counters."""
        self.total_requests = 0
        self.total_errors = 0
        self.total_high_risk = 0
        self.total_manual_review = 0
        self.total_blocked = 0
        self.average_latency_ms = 0.0

    def record_request(
        self,
        latency_ms: float,
        risk_level: str | None = None,
        decision: str | None = None,
    ) -> None:
        """Record a processed request and update aggregate metrics."""
        previous_total = self.total_requests
        self.total_requests += 1
        self.average_latency_ms = (
            (self.average_latency_ms * previous_total) + latency_ms
        ) / self.total_requests

        if risk_level == "high":
            self.total_high_risk += 1
        if decision == "manual_review":
            self.total_manual_review += 1
        if decision == "blocked":
            self.total_blocked += 1

    def record_error(self) -> None:
        """Record a failed request."""
        self.total_errors += 1

    def get_metrics(self) -> dict[str, int | float]:
        """Return a snapshot of all metrics."""
        return {
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "total_high_risk": self.total_high_risk,
            "total_manual_review": self.total_manual_review,
            "total_blocked": self.total_blocked,
            "average_latency_ms": round(self.average_latency_ms, 3),
        }

    def record_incident(self) -> None:
        """Record one analyzed incident for current API compatibility."""
        self.record_request(latency_ms=0.0)

    def snapshot(self) -> dict[str, int | float]:
        """Return current metrics for current API compatibility."""
        return self.get_metrics()
