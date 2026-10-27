"""Tests for safe configuration loading and defaults."""

from app.core.config import Settings


def test_settings_load_with_safe_defaults():
    """Verify settings initialize cleanly without requiring external secrets."""
    test_settings = Settings()

    assert test_settings.PROJECT_NAME == "SkyOps Intelligence Backend"
    assert test_settings.ENVIRONMENT == "development"
    assert test_settings.API_V1_PREFIX == "/api/v1"
    assert test_settings.BACKEND_PORT == 8000
    assert isinstance(test_settings.CORS_ORIGINS, list)
    assert len(test_settings.CORS_ORIGINS) > 0
    assert test_settings.DEFAULT_LLM_MODEL == "claude-3-5-sonnet-20241022"
    assert test_settings.DEFAULT_EMBEDDING_MODEL == "text-embedding-3-large"
    assert test_settings.LLM_TEMPERATURE == 0.0


def test_settings_custom_override():
    """Verify settings can be overridden safely via parameters."""
    custom_settings = Settings(
        ENVIRONMENT="staging",
        DEBUG=False,
        BACKEND_PORT=9000,
    )
    assert custom_settings.ENVIRONMENT == "staging"
    assert custom_settings.DEBUG is False
    assert custom_settings.BACKEND_PORT == 9000
