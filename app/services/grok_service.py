"""Centralized Grok service using the OpenAI-compatible xAI API."""

import json
from os import getenv
from typing import Any


class GrokServiceError(RuntimeError):
    """Raised when the Grok API call fails."""


class GrokParsingError(ValueError):
    """Raised when a Grok response cannot be parsed as JSON."""


class GrokService:
    """Call Grok through xAI's OpenAI-compatible chat completions API."""

    def __init__(
        self,
        client: Any | None = None,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        """Initialize the Grok service with an injectable client."""
        self.api_key = api_key or getenv("GROK_API_KEY")
        self.model = model or getenv("GROK_MODEL", "grok-2-latest")
        self.base_url = base_url or getenv("GROK_API_BASE_URL", "https://api.x.ai/v1")
        self._client = client

    def call_grok(self, system_prompt: str, user_prompt: str) -> str:
        """Call Grok and return the raw text response."""
        client = self._get_client()
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return self._extract_content(response)
        except GrokServiceError:
            raise
        except Exception as exc:
            raise GrokServiceError(f"Grok API call failed: {exc}") from exc

    def call_grok_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Call Grok with strict JSON output and return the parsed object."""
        client = self._get_client()
        json_system_prompt = (
            f"{system_prompt}\n"
            "Return only one valid JSON object. Do not include Markdown, prose, or code fences."
        )
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": json_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
            return self.parse_json_response(self._extract_content(response))
        except GrokParsingError:
            raise
        except GrokServiceError:
            raise
        except Exception as exc:
            raise GrokServiceError(f"Grok JSON API call failed: {exc}") from exc

    def parse_json_response(self, response: str) -> dict[str, Any]:
        """Parse a direct JSON response or a fenced ```json response."""
        cleaned_response = self._strip_json_fence(response)
        try:
            parsed = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise GrokParsingError(f"Invalid JSON response from Grok: {exc.msg}") from exc

        if not isinstance(parsed, dict):
            raise GrokParsingError("Invalid JSON response from Grok: expected a JSON object")
        return parsed

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self.api_key:
            raise GrokServiceError("GROK_API_KEY is required to initialize GrokService")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise GrokServiceError("The openai package is required to use GrokService") from exc

        self._client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        return self._client

    def _extract_content(self, response: Any) -> str:
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError, TypeError) as exc:
            raise GrokServiceError("Grok response did not contain message content") from exc

        if not isinstance(content, str) or not content.strip():
            raise GrokServiceError("Grok response content is empty")
        return content

    def _strip_json_fence(self, response: str) -> str:
        stripped = response.strip()
        if stripped.startswith("```json") and stripped.endswith("```"):
            return stripped.removeprefix("```json").removesuffix("```").strip()
        if stripped.startswith("```") and stripped.endswith("```"):
            return stripped.removeprefix("```").removesuffix("```").strip()
        return stripped
