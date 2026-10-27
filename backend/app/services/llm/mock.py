"""Mock LLM client adapter for automated testing and offline development."""

import time

from app.services.llm.base import (
    BaseLLMClient,
    ChatMessage,
    LLMConfigurationError,
    LLMInvalidResponseError,
    LLMProviderError,
    LLMRateLimitError,
    LLMResponse,
    LLMTimeoutError,
)


class MockLLMClient(BaseLLMClient):
    """Deterministic mock client for running tests without paid API keys or network calls."""

    def __init__(
        self,
        default_response: str = "Mock SkyOps LLM Response: Procedure verified active in GOM.",
        model_name: str = "mock-aviation-model",
        should_timeout: bool = False,
        should_rate_limit: bool = False,
        should_fail_provider: bool = False,
        should_return_invalid: bool = False,
        should_fail_config: bool = False,
    ):
        self.default_response = default_response
        self.model_name = model_name
        self.should_timeout = should_timeout
        self.should_rate_limit = should_rate_limit
        self.should_fail_provider = should_fail_provider
        self.should_return_invalid = should_return_invalid
        self.should_fail_config = should_fail_config
        self.call_history: list[list[ChatMessage]] = []
        self.canned_responses: dict[str, str] = {}

    def register_canned_response(self, keyword: str, response: str) -> None:
        """Register a specific response mapped to a keyword in user message."""
        self.canned_responses[keyword.lower()] = response

    def _execute(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        start_time = time.perf_counter()
        self.call_history.append(messages)

        if self.should_fail_config:
            raise LLMConfigurationError(
                message="Mock configuration failure: API key or model missing",
                provider="mock",
            )

        if self.should_timeout:
            raise LLMTimeoutError(
                message="Mock request timed out after 30.0s",
                provider="mock",
            )

        if self.should_rate_limit:
            raise LLMRateLimitError(
                message="Mock provider rate limit exceeded (HTTP 429)",
                provider="mock",
            )

        if self.should_fail_provider:
            raise LLMProviderError(
                message="Mock provider internal server error (HTTP 500)",
                provider="mock",
            )

        if self.should_return_invalid:
            raise LLMInvalidResponseError(
                message="Mock provider returned an empty or malformed payload",
                provider="mock",
            )

        # Check for canned keyword responses
        selected_text = self.default_response
        for msg in messages:
            content_lower = msg.content.lower()
            for kw, resp in self.canned_responses.items():
                if kw in content_lower:
                    selected_text = resp
                    break

        latency = (time.perf_counter() - start_time) * 1000

        return LLMResponse(
            content=selected_text,
            model=self.model_name,
            usage={"prompt_tokens": 42, "completion_tokens": 18, "total_tokens": 60},
            finish_reason="stop",
            provider="mock",
            latency_ms=round(latency, 2),
        )

    def complete(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        return self._execute(messages, temperature, max_tokens)

    async def acomplete(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        return self._execute(messages, temperature, max_tokens)
