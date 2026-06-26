"""Local toxicity checker."""

import re

TOXIC_KEYWORDS = frozenset({"hate", "threat", "kill", "abuse", "harass", "violence"})


def check_toxicity(text: str) -> dict[str, float | str | list[str]]:
    """Return a deterministic toxicity score and status."""
    lowered = text.lower()
    matched_terms = sorted(
        keyword for keyword in TOXIC_KEYWORDS if re.search(rf"\b{re.escape(keyword)}\b", lowered)
    )
    score = min(1.0, round(len(matched_terms) / 3, 3))
    return {
        "score": score,
        "status": "unsafe" if matched_terms else "safe",
        "matched_terms": matched_terms,
    }


class ToxicityChecker:
    """Detect a small set of toxic terms locally."""

    def check(self, text: str) -> dict[str, float | str | list[str]]:
        """Return a deterministic toxicity check result."""
        return check_toxicity(text)

    def detect(self, text: str) -> bool:
        """Return whether text is unsafe."""
        return check_toxicity(text)["status"] == "unsafe"
