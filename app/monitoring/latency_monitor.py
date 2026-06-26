"""Latency monitoring helpers."""

from time import perf_counter


class LatencyMonitor:
    """Measure elapsed processing time in milliseconds."""

    def __init__(self) -> None:
        """Initialize the latency monitor."""
        self._start_time: float | None = None

    def start_timer(self) -> None:
        """Start an internal timer."""
        self._start_time = perf_counter()

    def stop_timer(self) -> float:
        """Stop the internal timer and return elapsed milliseconds."""
        if self._start_time is None:
            return 0.0
        elapsed = round((perf_counter() - self._start_time) * 1000, 3)
        self._start_time = None
        return elapsed

    def start(self) -> float:
        """Return a monotonic start timestamp."""
        return perf_counter()

    def elapsed_ms(self, start_time: float) -> float:
        """Return elapsed time in milliseconds."""
        return round((perf_counter() - start_time) * 1000, 3)
