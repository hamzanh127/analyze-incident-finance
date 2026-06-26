"""Local prompt injection checker."""

PROMPT_INJECTION_PATTERNS = (
    "ignore previous instructions",
    "reveal system prompt",
    "dump database",
    "bypass security",
)


def detect_prompt_injection(text: str) -> dict[str, bool | list[str]]:
    """Detect known prompt injection patterns."""
    lowered = text.lower()
    matched_patterns = [pattern for pattern in PROMPT_INJECTION_PATTERNS if pattern in lowered]
    return {
        "detected": bool(matched_patterns),
        "matched_patterns": matched_patterns,
    }


class PromptInjectionChecker:
    """Detect common prompt injection patterns."""

    def check(self, text: str) -> dict[str, bool | list[str]]:
        """Return a deterministic prompt injection check result."""
        return detect_prompt_injection(text)

    def detect(self, text: str) -> bool:
        """Return whether text contains prompt injection patterns."""
        return bool(detect_prompt_injection(text)["detected"])
