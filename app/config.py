"""Application configuration."""

from functools import lru_cache
from os import getenv

from pydantic import BaseModel, Field

from app.utils.constants import DEFAULT_ENVIRONMENT, DEFAULT_LOG_LEVEL, SERVICE_NAME, SERVICE_VERSION


class Settings(BaseModel):
    """Runtime settings for the finance incident multi-agent service."""

    app_name: str = Field(default=SERVICE_NAME)
    app_version: str = Field(default=SERVICE_VERSION)
    environment: str = Field(default=DEFAULT_ENVIRONMENT)
    debug: bool = Field(default=False)
    log_level: str = Field(default=DEFAULT_LOG_LEVEL)
    enable_monitoring: bool = Field(default=True)

    @classmethod
    def from_environment(cls) -> "Settings":
        """Build settings from environment variables."""
        return cls(
            app_name=getenv("APP_NAME", SERVICE_NAME),
            app_version=getenv("APP_VERSION", SERVICE_VERSION),
            environment=getenv("ENVIRONMENT", DEFAULT_ENVIRONMENT),
            debug=_get_bool("DEBUG", default=False),
            log_level=getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper(),
            enable_monitoring=_get_bool("ENABLE_MONITORING", default=True),
        )


def _get_bool(name: str, default: bool) -> bool:
    raw_value = getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings.from_environment()


settings = get_settings()
