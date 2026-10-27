# LLM Client Adapter & Completion Guide
## SkyOps Intelligence: LLM API Integration & First Completion

**Document Status:** Approved Baseline  
**Target Milestone:** 3.12 (LLM API Access & First Completion)  
**Effective Date:** 2026-10-27  

---

## 1. Overview & Architecture

SkyOps Intelligence requires deterministic, low-latency, and safety-constrained completions. The LLM client layer is decoupled from underlying API providers via a standardized adapter pattern (`BaseLLMClient`):

```
                   +----------------------------------+
                   |          BaseLLMClient          |
                   |   .complete(messages, temp=0.0)  |
                   |   .acomplete(messages, temp=0.0) |
                   +-----------------+----------------+
                                     |
              +----------------------+----------------------+
              |                                             |
              v                                             v
  +-----------------------+                     +-----------------------+
  |     MockLLMClient     |                     |    OpenAILLMClient    |
  | (Offline, Zero Cost,  |                     | (OpenAI / Azure /     |
  |  Simulated Failures)  |                     |  Compatible Endpoints)|
  +-----------------------+                     +-----------------------+
```

---

## 2. Configuration & Environment Variables

Credentials and model settings are read safely from environment variables or `.env`:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `LLM_PROVIDER` | `mock` | Active provider: `mock` (zero-cost offline testing) or `openai`. |
| `OPENAI_API_KEY` | `None` | API key for OpenAI or compatible provider. **Never commit real keys.** |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Base URL for API calls. Can point to local LLM proxies (e.g., vLLM / Ollama). |
| `DEFAULT_LLM_MODEL` | `gpt-4o-mini` | Default chat model identifier. |
| `LLM_TEMPERATURE` | `0.0` | Sampling temperature ($0.0$ for deterministic aviation procedures). |
| `LLM_REQUEST_TIMEOUT_SECONDS` | `30.0` | Maximum timeout before raising `LLMTimeoutError`. |
| `LLM_MAX_RETRIES` | `2` | Number of retries on transient connection failures. |

---

## 3. Error Handling & Safety Domain Exceptions

All raw HTTP and provider errors are mapped to standardized domain exceptions:

1. **`LLMConfigurationError`:** Raised when required credentials (`OPENAI_API_KEY`) are missing, empty, or contain placeholder text, or upon HTTP 401/403.
2. **`LLMTimeoutError`:** Raised when a provider fails to respond within `LLM_REQUEST_TIMEOUT_SECONDS`.
3. **`LLMRateLimitError`:** Raised upon HTTP 429 rate limit errors with exponential backoff triggers.
4. **`LLMProviderError`:** Raised upon provider outages (HTTP 500, 502, 503, 504) or network transport breaks.
5. **`LLMInvalidResponseError`:** Raised if the provider emits empty, malformed, or invalid JSON.

---

## 4. Running the Smoke Test

### A. Offline Mock Mode (Zero Cost)
```bash
python backend/scripts/smoke_test_llm.py --mock
```

### B. Live Real Provider Mode
```bash
export OPENAI_API_KEY="sk-your-real-key"
python backend/scripts/smoke_test_llm.py
```
*If credentials are not configured, the script gracefully reports `[STATUS] SKIPPED: Live API credentials (OPENAI_API_KEY) are not configured.` without failing.*
