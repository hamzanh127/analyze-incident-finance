"""In-memory metrics collector."""


class MetricsCollector:
    """Collect monitoring counters in memory."""

    def __init__(self) -> None:
        """Initialize metric counters."""
        self.requests = 0
        self.errors = 0
        self.prompt_injections = 0
        self.pii_detections = 0

    def record_request(self) -> None:
        """Increment the request counter."""
        self.requests += 1

    def record_error(self) -> None:
        """Increment the error counter."""
        self.errors += 1

    def record_prompt_injection(self) -> None:
        """Increment the prompt injection counter."""
        self.prompt_injections += 1

    def record_pii_detection(self) -> None:
        """Increment the PII detection counter."""
        self.pii_detections += 1

    def get_metrics(self) -> dict[str, int]:
        """Return a copy of monitoring counters."""
        return {
            "requests": self.requests,
            "errors": self.errors,
            "prompt_injections": self.prompt_injections,
            "pii_detections": self.pii_detections,
        }

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a named counter for compatibility."""
        if not hasattr(self, name):
            setattr(self, name, 0)
        current_value = getattr(self, name)
        if isinstance(current_value, int):
            setattr(self, name, current_value + value)

    def snapshot(self) -> dict[str, int]:
        """Return a copy of collected counters."""
        return self.get_metrics()
