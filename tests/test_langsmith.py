"""Tests for LangSmith observability configuration."""

from unittest.mock import MagicMock

import pytest

from app.config import LANGSMITH_DEFAULT_ENDPOINT, LANGSMITH_DEFAULT_PROJECT, Settings, get_settings
from app.monitoring import langsmith_tracing


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Keep environment-based settings isolated per test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_langsmith_configuration_loads_from_environment(monkeypatch) -> None:
    """Settings load LangSmith values from environment variables."""
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    monkeypatch.setenv("LANGSMITH_API_KEY", "test-key")
    monkeypatch.setenv("LANGSMITH_PROJECT", "finance-incident-multi-agent")
    monkeypatch.setenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.langsmith_tracing is True
    assert settings.langsmith_enabled is True
    assert settings.langsmith_project == LANGSMITH_DEFAULT_PROJECT
    assert settings.langsmith_endpoint == LANGSMITH_DEFAULT_ENDPOINT


def test_langsmith_tracing_is_disabled_without_api_key(monkeypatch) -> None:
    """Tracing is effectively disabled when no API key is configured."""
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.langsmith_tracing is True
    assert settings.langsmith_enabled is False


def test_langsmith_status_reports_correct_configuration() -> None:
    """The public observability payload exposes the effective tracing status."""
    settings = Settings(
        environment="test",
        app_version="9.9.9",
        langsmith_tracing=True,
        langsmith_api_key="test-key",
        langsmith_project="finance-incident-multi-agent",
        langsmith_endpoint="https://api.smith.langchain.com",
    )

    status = langsmith_tracing.langsmith_status(settings)

    assert status == {
        "langsmith_enabled": True,
        "project": "finance-incident-multi-agent",
        "tracing": True,
        "environment": "test",
        "version": "9.9.9",
    }


def test_trace_step_does_not_call_langsmith_when_disabled(monkeypatch) -> None:
    """Disabled tracing executes the function without contacting LangSmith."""
    settings = Settings(langsmith_tracing=True, langsmith_api_key="")
    monkeypatch.setattr(langsmith_tracing, "get_settings", lambda: settings)
    traceable_mock = MagicMock()
    monkeypatch.setattr(langsmith_tracing, "traceable", traceable_mock)

    result = langsmith_tracing.trace_step("Risk Agent", {}, lambda: {"ok": True})

    assert result == {"ok": True}
    traceable_mock.assert_not_called()


def test_trace_step_uses_mocked_traceable_when_enabled(monkeypatch) -> None:
    """Enabled tracing wraps the function with the LangSmith traceable decorator."""
    settings = Settings(langsmith_tracing=True, langsmith_api_key="test-key")
    monkeypatch.setattr(langsmith_tracing, "get_settings", lambda: settings)

    def fake_traceable(**kwargs):
        assert kwargs["name"] == "Risk Agent"
        assert kwargs["run_type"] == "chain"

        def decorator(func):
            return func

        return decorator

    monkeypatch.setattr(langsmith_tracing, "traceable", fake_traceable)

    result = langsmith_tracing.trace_step("Risk Agent", {}, lambda: {"ok": True})

    assert result == {"ok": True}
