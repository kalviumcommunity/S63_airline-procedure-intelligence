"""Factory for instantiating configured LLM client adapters."""

import logging

from app.core.config import Settings
from app.core.config import settings as default_settings
from app.services.llm.base import BaseLLMClient
from app.services.llm.mock import MockLLMClient
from app.services.llm.provider import OpenAILLMClient

logger = logging.getLogger(__name__)


def get_llm_client(app_settings: Settings | None = None) -> BaseLLMClient:
    """Instantiate and return the appropriate LLM client based on application settings.

    - If LLM_PROVIDER is 'mock' or credentials are not configured, returns MockLLMClient.
    - If LLM_PROVIDER is 'openai', returns OpenAILLMClient initialized with environment credentials.
    """
    cfg = app_settings or default_settings
    provider = cfg.LLM_PROVIDER.lower().strip()

    if provider == "mock":
        logger.info("Initializing MockLLMClient for offline / mock testing execution.")
        return MockLLMClient(
            model_name=cfg.DEFAULT_LLM_MODEL,
        )

    if provider == "openai":
        return OpenAILLMClient(
            api_key=cfg.OPENAI_API_KEY,
            model_name=cfg.DEFAULT_LLM_MODEL,
            base_url=cfg.OPENAI_BASE_URL,
            timeout_seconds=cfg.LLM_REQUEST_TIMEOUT_SECONDS,
            max_retries=cfg.LLM_MAX_RETRIES,
        )

    # Default fallback to mock with warning
    logger.warning(
        f"Unrecognized or unconfigured LLM_PROVIDER '{cfg.LLM_PROVIDER}'. Falling back to MockLLMClient."
    )
    return MockLLMClient(model_name=cfg.DEFAULT_LLM_MODEL)
