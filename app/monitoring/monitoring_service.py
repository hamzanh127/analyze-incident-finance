"""Central monitoring service."""

from app.monitoring.cost_monitor import estimate_cost
from app.monitoring.hallucination_checker import check_hallucination
from app.monitoring.metrics_collector import MetricsCollector
from app.monitoring.pii_checker import detect_pii
from app.monitoring.prompt_injection_checker import detect_prompt_injection
from app.monitoring.token_monitor import estimate_tokens
from app.monitoring.toxicity_checker import check_toxicity


class MonitoringService:
    """Run deterministic local monitoring checks over text."""

    def __init__(self, metrics_collector: MetricsCollector | None = None) -> None:
        """Initialize monitoring dependencies."""
        self._metrics_collector = metrics_collector or MetricsCollector()

    def analyze_text(self, text: str) -> dict[str, object]:
        """Analyze text for safety, usage, and estimated cost."""
        self._metrics_collector.record_request()
        toxicity = check_toxicity(text)
        hallucination = check_hallucination(text)
        prompt_injection = detect_prompt_injection(text)
        pii = detect_pii(text)
        tokens = estimate_tokens(text)
        estimated_tokens = int(tokens["estimated_tokens"])
        cost = estimate_cost(input_tokens=estimated_tokens, output_tokens=0)

        if bool(prompt_injection["detected"]):
            self._metrics_collector.record_prompt_injection()
        if bool(pii["detected"]):
            self._metrics_collector.record_pii_detection()

        safe = (
            toxicity["status"] == "safe"
            and not bool(prompt_injection["detected"])
            and not bool(pii["detected"])
        )
        return {
            "safe": safe,
            "toxicity": toxicity,
            "hallucination": hallucination,
            "prompt_injection": prompt_injection,
            "pii": pii,
            "tokens": tokens,
            "cost": cost,
            "metrics": self._metrics_collector.get_metrics(),
        }

    def evaluate(self, text: str) -> dict[str, bool]:
        """Evaluate text with boolean checks for current agent compatibility."""
        result = self.analyze_text(text)
        return {
            "toxic": result["toxicity"]["status"] == "unsafe",  # type: ignore[index]
            "hallucination_risk": result["hallucination"]["risk_level"] != "low",  # type: ignore[index]
            "prompt_injection": bool(result["prompt_injection"]["detected"]),  # type: ignore[index]
            "pii_detected": bool(result["pii"]["detected"]),  # type: ignore[index]
        }
