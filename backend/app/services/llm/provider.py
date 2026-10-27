"""Production LLM client adapter for OpenAI and compatible HTTP APIs."""

import json
import time

import httpx

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


class OpenAILLMClient(BaseLLMClient):
    """Client adapter connecting to OpenAI Chat Completions API or compatible endpoints."""

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        timeout_seconds: float = 30.0,
        max_retries: int = 2,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate that the client has a potentially valid API key."""
        if not self.api_key or self.api_key.strip() == "":
            raise LLMConfigurationError(
                message="OPENAI_API_KEY is not configured or is empty. Set OPENAI_API_KEY in environment or .env.",
                provider="openai",
            )
        if self.api_key.startswith("sk-placeholder") or "placeholder" in self.api_key.lower():
            raise LLMConfigurationError(
                message="OPENAI_API_KEY contains placeholder text. Configure a valid key for live completions.",
                provider="openai",
            )

    def _prepare_payload(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> dict:
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        payload: dict = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        return payload

    def _parse_response(self, response: httpx.Response, latency_ms: float) -> LLMResponse:
        """Parse raw HTTP response and map error status codes to domain exceptions."""
        if response.status_code == 401 or response.status_code == 403:
            raise LLMConfigurationError(
                message=f"Authentication failed with OpenAI API (HTTP {response.status_code}): {response.text}",
                provider="openai",
                details={"status_code": response.status_code, "body": response.text},
            )

        if response.status_code == 429:
            raise LLMRateLimitError(
                message="OpenAI API rate limit exceeded (HTTP 429). Retry after backoff.",
                provider="openai",
                details={"body": response.text},
            )

        if response.status_code >= 500:
            raise LLMProviderError(
                message=f"OpenAI service error (HTTP {response.status_code}): {response.text}",
                provider="openai",
                details={"status_code": response.status_code},
            )

        if response.status_code != 200:
            raise LLMProviderError(
                message=f"Unexpected OpenAI response status (HTTP {response.status_code}): {response.text}",
                provider="openai",
                details={"status_code": response.status_code},
            )

        try:
            data = response.json()
        except json.JSONDecodeError as exc:
            raise LLMInvalidResponseError(
                message="Failed to parse JSON response from OpenAI API",
                provider="openai",
            ) from exc

        choices = data.get("choices")
        if not choices or not isinstance(choices, list) or len(choices) == 0:
            raise LLMInvalidResponseError(
                message="OpenAI response contained empty or missing 'choices' list",
                provider="openai",
                details=data,
            )

        message_obj = choices[0].get("message", {})
        content = message_obj.get("content")
        if content is None:
            raise LLMInvalidResponseError(
                message="OpenAI response choice did not contain message content",
                provider="openai",
                details=choices[0],
            )

        usage = data.get("usage", {})

        return LLMResponse(
            content=content,
            model=data.get("model", self.model_name),
            usage=usage,
            finish_reason=choices[0].get("finish_reason", "stop"),
            provider="openai",
            latency_ms=round(latency_ms, 2),
        )

    def complete(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = self._prepare_payload(messages, temperature, max_tokens)

        start_time = time.perf_counter()
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(endpoint, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(
                message=f"OpenAI API request timed out after {self.timeout_seconds}s",
                provider="openai",
            ) from exc
        except httpx.RequestError as exc:
            raise LLMProviderError(
                message=f"Network error connecting to OpenAI API: {str(exc)}",
                provider="openai",
            ) from exc

        latency_ms = (time.perf_counter() - start_time) * 1000
        return self._parse_response(response, latency_ms)

    async def acomplete(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = self._prepare_payload(messages, temperature, max_tokens)

        start_time = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(endpoint, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(
                message=f"OpenAI API request timed out after {self.timeout_seconds}s",
                provider="openai",
            ) from exc
        except httpx.RequestError as exc:
            raise LLMProviderError(
                message=f"Network error connecting to OpenAI API: {str(exc)}",
                provider="openai",
            ) from exc

        latency_ms = (time.perf_counter() - start_time) * 1000
        return self._parse_response(response, latency_ms)
