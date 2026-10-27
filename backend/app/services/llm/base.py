"""Base interfaces, data structures, and exceptions for LLM client adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal


# ------------------------------------------------------------------------------
# Domain Exceptions
# ------------------------------------------------------------------------------
class LLMError(Exception):
    """Base exception for all LLM client failures."""

    def __init__(self, message: str, provider: str = "unknown", details: Any = None):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.details = details


class LLMConfigurationError(LLMError):
    """Raised when required credentials or settings are missing or invalid."""


class LLMTimeoutError(LLMError):
    """Raised when an LLM completion request exceeds the timeout deadline."""


class LLMRateLimitError(LLMError):
    """Raised when the LLM provider responds with rate limit exceeded (HTTP 429)."""


class LLMProviderError(LLMError):
    """Raised when the LLM provider experiences server errors (HTTP 5xx) or network failures."""


class LLMInvalidResponseError(LLMError):
    """Raised when the provider response is empty, malformed, or missing required fields."""


# ------------------------------------------------------------------------------
# Data Structures
# ------------------------------------------------------------------------------
@dataclass
class ChatMessage:
    """Standardized chat message payload."""

    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class LLMResponse:
    """Standardized response from an LLM completion."""

    content: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    provider: str = "unknown"
    latency_ms: float = 0.0


# ------------------------------------------------------------------------------
# Abstract Base Client
# ------------------------------------------------------------------------------
class BaseLLMClient(ABC):
    """Abstract Base Class for LLM client adapters."""

    @abstractmethod
    def complete(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Synchronously execute a chat completion."""
        pass

    @abstractmethod
    async def acomplete(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Asynchronously execute a chat completion."""
        pass

