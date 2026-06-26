"""Observability primitives."""

from dataclasses import dataclass
from datetime import UTC, datetime


def build_observability_event(
    correlation_id: str,
    agent_name: str,
    status: str,
    latency_ms: float | None = None,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    """Build a structured observability event."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "correlation_id": correlation_id,
        "agent_name": agent_name,
        "status": status,
        "latency_ms": latency_ms,
        "metadata": metadata or {},
    }


@dataclass(frozen=True)
class ObservabilityEvent:
    """Structured event emitted by local services."""

    name: str
    timestamp: datetime
    attributes: dict[str, str]


class Observability:
    """Create structured observability events."""

    def create_event(self, name: str, attributes: dict[str, str] | None = None) -> ObservabilityEvent:
        """Create a timestamped observability event."""
        return ObservabilityEvent(
            name=name,
            timestamp=datetime.now(UTC),
            attributes=attributes or {},
        )
