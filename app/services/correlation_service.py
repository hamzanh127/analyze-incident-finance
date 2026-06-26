"""Correlation service."""

from datetime import UTC, datetime
from secrets import token_hex


def generate_correlation_id() -> str:
    """Generate a finance correlation identifier."""
    date_part = datetime.now(UTC).strftime("%Y%m%d")
    random_part = token_hex(3).upper()
    return f"FIN-{date_part}-{random_part}"


class CorrelationService:
    """Provide correlation identifiers for request tracing."""

    def new_correlation_id(self) -> str:
        """Create a new correlation identifier."""
        return generate_correlation_id()
