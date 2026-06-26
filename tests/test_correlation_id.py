"""Tests for correlation identifiers."""

import re

from app.services.correlation_service import generate_correlation_id


def test_generate_correlation_id_format() -> None:
    """Generated correlation id matches FIN-YYYYMMDD-XXXXXX."""
    correlation_id = generate_correlation_id()

    assert re.fullmatch(r"FIN-\d{8}-[A-F0-9]{6}", correlation_id)
