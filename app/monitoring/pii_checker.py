"""Local PII checker."""

import re

PII_PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?){2,4}\d{2,4}\b"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", re.IGNORECASE),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
}


def detect_pii(text: str) -> dict[str, bool | list[str]]:
    """Detect simple PII patterns with regular expressions."""
    detected_types = [
        pii_type for pii_type, pattern in PII_PATTERNS.items() if pattern.search(text)
    ]
    return {
        "detected": bool(detected_types),
        "types": detected_types,
    }


class PiiChecker:
    """Detect simple personally identifiable information patterns."""

    def check(self, text: str) -> dict[str, bool | list[str]]:
        """Return a deterministic PII check result."""
        return detect_pii(text)

    def detect(self, text: str) -> bool:
        """Return whether text contains basic PII patterns."""
        return bool(detect_pii(text)["detected"])
