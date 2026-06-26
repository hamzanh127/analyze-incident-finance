"""General helper functions."""

from app.utils.constants import DEFAULT_CURRENCY


def normalize_text(value: str) -> str:
    """Normalize a user-provided text value."""
    return value.strip()


def normalize_currency(currency: str) -> str:
    """Normalize a currency code to uppercase."""
    normalized = normalize_text(currency).upper()
    return normalized or DEFAULT_CURRENCY


def normalize_country(country: str) -> str:
    """Normalize a country code or country label."""
    return normalize_text(country).upper()


def format_amount(amount: float, currency: str) -> str:
    """Format a money amount for logs and responses."""
    return f"{amount:.2f} {normalize_currency(currency)}"


def clamp_score(score: int, minimum: int = 0, maximum: int = 100) -> int:
    """Clamp a score to an inclusive numeric range."""
    return max(minimum, min(score, maximum))
