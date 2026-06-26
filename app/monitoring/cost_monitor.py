"""Cost monitoring helpers."""

INPUT_COST_PER_1K_TOKENS = 0.0001
OUTPUT_COST_PER_1K_TOKENS = 0.0002


def estimate_cost(input_tokens: int, output_tokens: int) -> dict[str, int | float]:
    """Estimate a simple local processing cost."""
    input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K_TOKENS
    output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K_TOKENS
    total_cost = round(input_cost + output_cost, 8)
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": total_cost,
        "currency": "USD",
    }


class CostMonitor:
    """Estimate local processing cost."""

    def estimate(self, tokens: int, cost_per_token: float = 0.0) -> float:
        """Return an estimated cost for a token count."""
        return round(tokens * cost_per_token, 6)
