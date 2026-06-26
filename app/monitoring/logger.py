"""Logging configuration helpers."""

import logging


def log_observability_event(event: dict[str, object]) -> dict[str, object]:
    """Return a structured observability event as the log payload."""
    return {
        "logged": True,
        "event": event,
    }


def get_logger(name: str) -> logging.Logger:
    """Return a configured application logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
