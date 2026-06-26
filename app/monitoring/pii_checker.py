"""Local PII checker."""

import re

PII_PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"(?:\+212|0)[ \-\.]?[567][ \-\.]?\d{2}[ \-\.]?\d{2}[ \-\.]?\d{2}[ \-\.]?\d{2}\b"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", re.IGNORECASE),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "cin": re.compile(r"\b[A-Z]{1,2}\d{4,6}\b", re.IGNORECASE),
    "name": re.compile(r"(?i)\b(?:nom|name|client)\s*[:=]\s*([a-zA-Z\s]+)"),
}


def detect_pii(text: str) -> dict[str, object]:
    """Detect simple PII patterns with regular expressions."""
    detected_types = []
    matches_count = 0
    for pii_type, pattern in PII_PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            detected_types.append(pii_type)
            matches_count += len(matches)

    return {
        "detected": bool(detected_types),
        "types": detected_types,
        "matches_count": matches_count,
    }


class PiiChecker:
    """Detect simple personally identifiable information patterns."""

    def check(self, text: str) -> dict[str, bool | list[str]]:
        """Return a deterministic PII check result."""
        return detect_pii(text)

    def detect(self, text: str) -> bool:
        """Return whether text contains basic PII patterns."""
        return bool(detect_pii(text)["detected"])
