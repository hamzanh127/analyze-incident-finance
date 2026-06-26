"""Application logging service."""

from datetime import UTC, datetime


def log_event(
    correlation_id: str,
    event_type: str,
    message: str,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    """Create a structured log event."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "correlation_id": correlation_id,
        "event_type": event_type,
        "message": message,
        "metadata": metadata or {},
    }


class LoggingService:
    """Create structured application log events."""

    def log_event(
        self,
        correlation_id: str,
        event_type: str,
        message: str,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Create a structured log event."""
        return log_event(correlation_id, event_type, message, metadata)

    def info(self, message: str, **extra: object) -> dict[str, object]:
        """Create an informational structured log event."""
        correlation_id = str(extra.pop("correlation_id", ""))
        return log_event(correlation_id, "info", message, extra)
