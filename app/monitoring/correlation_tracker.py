"""Correlation identifier tracking."""

import re
from uuid import uuid4

CORRELATION_ID_PATTERN = re.compile(r"^FIN-\d{8}-[A-F0-9]{6}$")


def validate_correlation_id(correlation_id: str) -> bool:
    """Return whether a correlation identifier matches the expected format."""
    return bool(CORRELATION_ID_PATTERN.fullmatch(correlation_id))


class CorrelationTracker:
    """Create and validate correlation identifiers."""

    def create_id(self) -> str:
        """Create a new correlation identifier."""
        return str(uuid4())

    def validate(self, correlation_id: str) -> bool:
        """Return whether a correlation identifier matches the expected format."""
        return validate_correlation_id(correlation_id)
