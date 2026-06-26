"""Local hallucination risk checker."""

STRONG_ASSERTIONS = (
    "guaranteed",
    "certainly",
    "always",
    "never",
    "proven",
    "without any doubt",
)


def check_hallucination(response: str, evidence: str | None = None) -> dict[str, str | bool | list[str]]:
    """Return a deterministic hallucination risk assessment."""
    lowered_response = response.lower()
    matched_assertions = [term for term in STRONG_ASSERTIONS if term in lowered_response]

    if evidence is None and matched_assertions:
        risk_level = "medium"
    elif evidence is not None and response.strip() and response.strip() not in evidence:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "evidence_provided": evidence is not None,
        "matched_assertions": matched_assertions,
    }


class HallucinationChecker:
    """Detect basic hallucination risk patterns in text."""

    def check(self, response: str, evidence: str | None = None) -> dict[str, str | bool | list[str]]:
        """Return a deterministic hallucination risk assessment."""
        return check_hallucination(response, evidence)

    def detect(self, text: str) -> bool:
        """Return whether hallucination risk is above low."""
        return check_hallucination(text)["risk_level"] != "low"
