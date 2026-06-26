"""Incident request schemas."""

from pydantic import BaseModel, Field, field_validator

from app.utils.helpers import normalize_country, normalize_currency, normalize_text


class IncidentRequest(BaseModel):
    """Input payload for finance incident analysis."""

    customer_id: str = Field(min_length=1, max_length=80)
    incident_type: str = Field(min_length=1, max_length=80)
    amount: float = Field(ge=0)
    currency: str = Field(min_length=1, max_length=3)
    country: str = Field(min_length=1, max_length=80)
    device: str = Field(min_length=1, max_length=120)
    beneficiary_status: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=2_000)

    @property
    def title(self) -> str:
        """Return a compatibility title derived from the incident type."""
        return self.incident_type

    @field_validator("customer_id", "incident_type", "device", "beneficiary_status", "description")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Validate and normalize required text fields."""
        normalized = normalize_text(value)
        if not normalized:
            raise ValueError("field must not be empty")
        return normalized

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        """Validate and normalize currency."""
        normalized = normalize_currency(value)
        if not normalized:
            raise ValueError("currency must not be empty")
        return normalized

    @field_validator("country")
    @classmethod
    def validate_country(cls, value: str) -> str:
        """Validate and normalize country."""
        normalized = normalize_country(value)
        if not normalized:
            raise ValueError("country must not be empty")
        return normalized
