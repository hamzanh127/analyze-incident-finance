"""Token usage estimation."""


def estimate_tokens(text: str) -> dict[str, int | float]:
    """Estimate tokens using a deterministic word multiplier."""
    word_count = len(text.split())
    estimated_tokens = int(round(word_count * 1.3))
    return {
        "word_count": word_count,
        "estimated_tokens": estimated_tokens,
        "multiplier": 1.3,
    }


class TokenMonitor:
    """Estimate token usage without external model calls."""

    def estimate(self, text: str) -> int:
        """Return the estimated token count."""
        return int(estimate_tokens(text)["estimated_tokens"])
