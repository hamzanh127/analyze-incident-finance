"""Chat schemas for the finance assistant endpoint."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatHistoryMessage(BaseModel):
    """A previous chat message sent back to preserve conversation context."""

    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1, max_length=4_000)


class ChatRequest(BaseModel):
    """Request payload for contextual finance incident chat."""

    message: str = Field(min_length=1, max_length=2_000)
    incident: dict[str, Any] | None = None
    analysis_result: dict[str, Any] | None = None
    history: list[ChatHistoryMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    """Response payload returned by the Grok-backed finance assistant."""

    message: str
    provider: str = "grok"
