"""Unit tests for LLM Client Adapters, Error Handling, and Mocks."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.core.config import Settings
from app.services.llm.base import (
    ChatMessage,
    LLMConfigurationError,
    LLMInvalidResponseError,
    LLMProviderError,
    LLMRateLimitError,
    LLMResponse,
    LLMTimeoutError,
)
from app.services.llm.factory import get_llm_client
from app.services.llm.mock import MockLLMClient
from app.services.llm.provider import OpenAILLMClient
from scripts.smoke_test_llm import run_smoke_test


# ------------------------------------------------------------------------------
# 1. Mock Client Tests
# ------------------------------------------------------------------------------
def test_mock_llm_client_default_completion():
    """Verify MockLLMClient returns valid deterministic response and tracks calls."""
    client = MockLLMClient()
    messages = [ChatMessage(role="user", content="Test procedure query")]

    response = client.complete(messages)

    assert isinstance(response, LLMResponse)
    assert response.provider == "mock"
    assert "Procedure verified" in response.content
    assert response.finish_reason == "stop"
    assert len(client.call_history) == 1
    assert client.call_history[0][0].content == "Test procedure query"


def test_mock_llm_client_canned_responses():
    """Verify canned responses match keyword triggers."""
    client = MockLLMClient()
    client.register_canned_response("fueling", "Fueling checklist: Connect bonding cable.")

    response = client.complete(
        [ChatMessage(role="user", content="Procedure for aircraft fueling?")]
    )
    assert response.content == "Fueling checklist: Connect bonding cable."

    # Non-matching query gets default
    response_default = client.complete([ChatMessage(role="user", content="Pushback procedure?")])
    assert "Procedure verified" in response_default.content


def test_mock_llm_client_timeout_handling():
    """Verify mock simulates timeout and raises LLMTimeoutError."""
    client = MockLLMClient(should_timeout=True)
    with pytest.raises(LLMTimeoutError) as exc_info:
        client.complete([ChatMessage(role="user", content="Test")])
    assert "timed out" in exc_info.value.message


def test_mock_llm_client_rate_limit_handling():
    """Verify mock simulates rate limit and raises LLMRateLimitError."""
    client = MockLLMClient(should_rate_limit=True)
    with pytest.raises(LLMRateLimitError) as exc_info:
        client.complete([ChatMessage(role="user", content="Test")])
    assert "rate limit" in exc_info.value.message.lower()


def test_mock_llm_client_provider_error_handling():
    """Verify mock simulates provider 500 error and raises LLMProviderError."""
    client = MockLLMClient(should_fail_provider=True)
    with pytest.raises(LLMProviderError) as exc_info:
        client.complete([ChatMessage(role="user", content="Test")])
    assert "500" in exc_info.value.message


def test_mock_llm_client_invalid_response_handling():
    """Verify mock simulates invalid response payload and raises LLMInvalidResponseError."""
    client = MockLLMClient(should_return_invalid=True)
    with pytest.raises(LLMInvalidResponseError) as exc_info:
        client.complete([ChatMessage(role="user", content="Test")])
    assert "malformed" in exc_info.value.message.lower()


def test_mock_llm_client_config_error_handling():
    """Verify mock simulates missing configuration and raises LLMConfigurationError."""
    client = MockLLMClient(should_fail_config=True)
    with pytest.raises(LLMConfigurationError) as exc_info:
        client.complete([ChatMessage(role="user", content="Test")])
    assert "configuration failure" in exc_info.value.message.lower()


# ------------------------------------------------------------------------------
# 2. OpenAI Provider Configuration & Validation Tests
# ------------------------------------------------------------------------------
def test_openai_client_rejects_missing_api_key():
    """Verify client rejects empty or None API key with LLMConfigurationError."""
    with pytest.raises(LLMConfigurationError) as exc_info:
        OpenAILLMClient(api_key=None)
    assert "OPENAI_API_KEY is not configured" in exc_info.value.message

    with pytest.raises(LLMConfigurationError):
        OpenAILLMClient(api_key="   ")


def test_openai_client_rejects_placeholder_api_key():
    """Verify client rejects dummy placeholder API keys."""
    with pytest.raises(LLMConfigurationError) as exc_info:
        OpenAILLMClient(api_key="sk-placeholder-openai-api-key")
    assert "placeholder" in exc_info.value.message.lower()


# ------------------------------------------------------------------------------
# 3. OpenAI Client HTTP Response & Error Mapping Tests
# ------------------------------------------------------------------------------
def test_openai_client_parses_valid_response():
    """Verify OpenAILLMClient correctly extracts content, model, and usage from 200 OK."""
    client = OpenAILLMClient(api_key="sk-valid-test-key-1234567890")

    mock_http_response = MagicMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = {
        "model": "gpt-4o-mini-2024-07-18",
        "choices": [
            {
                "message": {"role": "assistant", "content": "GOM 5.3 verified active."},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 15, "completion_tokens": 8, "total_tokens": 23},
    }

    with patch("httpx.Client.post", return_value=mock_http_response):
        response = client.complete([ChatMessage(role="user", content="Hello")])
        assert response.content == "GOM 5.3 verified active."
        assert response.model == "gpt-4o-mini-2024-07-18"
        assert response.usage["total_tokens"] == 23
        assert response.provider == "openai"


def test_openai_client_maps_401_authentication_error():
    """Verify HTTP 401 maps to LLMConfigurationError."""
    client = OpenAILLMClient(api_key="sk-valid-format-key-12345678")

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 401
    mock_resp.text = "Incorrect API key provided"

    with patch("httpx.Client.post", return_value=mock_resp):
        with pytest.raises(LLMConfigurationError) as exc_info:
            client.complete([ChatMessage(role="user", content="Hi")])
        assert "Authentication failed" in exc_info.value.message


def test_openai_client_maps_429_rate_limit():
    """Verify HTTP 429 maps to LLMRateLimitError."""
    client = OpenAILLMClient(api_key="sk-valid-format-key-12345678")

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 429
    mock_resp.text = "Rate limit reached"

    with patch("httpx.Client.post", return_value=mock_resp):
        with pytest.raises(LLMRateLimitError) as exc_info:
            client.complete([ChatMessage(role="user", content="Hi")])
        assert "rate limit exceeded" in exc_info.value.message.lower()


def test_openai_client_maps_500_provider_error():
    """Verify HTTP 500 maps to LLMProviderError."""
    client = OpenAILLMClient(api_key="sk-valid-format-key-12345678")

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 500
    mock_resp.text = "Internal Server Error"

    with patch("httpx.Client.post", return_value=mock_resp):
        with pytest.raises(LLMProviderError) as exc_info:
            client.complete([ChatMessage(role="user", content="Hi")])
        assert "OpenAI service error" in exc_info.value.message


def test_openai_client_maps_timeout_exception():
    """Verify httpx.TimeoutException maps to LLMTimeoutError."""
    client = OpenAILLMClient(api_key="sk-valid-format-key-12345678")

    with patch("httpx.Client.post", side_effect=httpx.ReadTimeout("Read timed out")):
        with pytest.raises(LLMTimeoutError) as exc_info:
            client.complete([ChatMessage(role="user", content="Hi")])
        assert "timed out" in exc_info.value.message


def test_openai_client_maps_malformed_json_response():
    """Verify non-JSON response maps to LLMInvalidResponseError."""
    client = OpenAILLMClient(api_key="sk-valid-format-key-12345678")

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200
    mock_resp.json.side_effect = ValueError("No JSON object could be decoded")

    with patch("httpx.Client.post", return_value=mock_resp):
        with pytest.raises(LLMInvalidResponseError) as exc_info:
            client.complete([ChatMessage(role="user", content="Hi")])
        assert "Failed to parse JSON" in exc_info.value.message


def test_openai_client_maps_missing_choices():
    """Verify response lacking choices array maps to LLMInvalidResponseError."""
    client = OpenAILLMClient(api_key="sk-valid-format-key-12345678")

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"id": "chat-123", "choices": []}

    with patch("httpx.Client.post", return_value=mock_resp):
        with pytest.raises(LLMInvalidResponseError) as exc_info:
            client.complete([ChatMessage(role="user", content="Hi")])
        assert "empty or missing 'choices'" in exc_info.value.message


# ------------------------------------------------------------------------------
# 4. Factory & Smoke Test Script Tests
# ------------------------------------------------------------------------------
def test_factory_returns_mock_client():
    """Verify factory returns MockLLMClient when provider is mock."""
    test_settings = Settings(LLM_PROVIDER="mock")
    client = get_llm_client(test_settings)
    assert isinstance(client, MockLLMClient)


def test_smoke_test_script_mock_mode():
    """Verify smoke test script executes cleanly in mock mode."""
    exit_code = run_smoke_test(use_mock=True)
    assert exit_code == 0


def test_smoke_test_script_unconfigured_real_mode():
    """Verify smoke test script gracefully skips when credentials are unconfigured."""
    with patch.dict("os.environ", {}, clear=True):
        exit_code = run_smoke_test(use_mock=False)
        assert exit_code == 0
