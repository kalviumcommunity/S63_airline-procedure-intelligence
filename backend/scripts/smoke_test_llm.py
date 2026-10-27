#!/usr/bin/env python3
"""Smoke test script for SkyOps LLM Client Adapter.

Usage:
    # Run mock adapter test:
    python backend/scripts/smoke_test_llm.py --mock

    # Run real API smoke test (requires OPENAI_API_KEY in environment):
    python backend/scripts/smoke_test_llm.py
"""

import argparse
import os
import sys
import time

# Ensure backend directory is in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.config import Settings  # noqa: E402
from app.services.llm.base import ChatMessage, LLMConfigurationError, LLMError  # noqa: E402
from app.services.llm.mock import MockLLMClient  # noqa: E402
from app.services.llm.provider import OpenAILLMClient  # noqa: E402


def run_smoke_test(use_mock: bool = False) -> int:
    """Execute LLM client smoke test and report result honestly."""
    print("=" * 70)
    print("SkyOps Intelligence - LLM Client Smoke Test (Milestone 3.12)")
    print("=" * 70)

    cfg = Settings()

    if use_mock:
        print("[MODE] Running MOCK LLM Adapter Test (Offline, zero cost)...")
        client = MockLLMClient(
            default_response="Operational Procedure Verified: Fueling supervisor must notify flight deck.",
            model_name="mock-aviation-model",
        )
    else:
        api_key = os.getenv("OPENAI_API_KEY") or cfg.OPENAI_API_KEY
        if not api_key or "placeholder" in api_key.lower():
            print("[STATUS] SKIPPED: Live API credentials (OPENAI_API_KEY) are not configured.")
            print("         A valid paid API key was not detected in environment or .env.")
            print("         To test with real provider:")
            print("             export OPENAI_API_KEY='sk-your-real-key'")
            print("             python backend/scripts/smoke_test_llm.py")
            print("         Or test offline adapter logic:")
            print("             python backend/scripts/smoke_test_llm.py --mock")
            print("=" * 70)
            return 0  # Clean skip, reported honestly

        print(f"[MODE] Running REAL API Smoke Test via OpenAI ({cfg.DEFAULT_LLM_MODEL})...")
        try:
            client = OpenAILLMClient(
                api_key=api_key,
                model_name=cfg.DEFAULT_LLM_MODEL,
                base_url=cfg.OPENAI_BASE_URL,
                timeout_seconds=cfg.LLM_REQUEST_TIMEOUT_SECONDS,
            )
        except LLMConfigurationError as err:
            print(f"[ERROR] Configuration validation failed: {err.message}")
            return 1

    # Formulate test aviation operational prompt
    messages = [
        ChatMessage(
            role="system",
            content="You are SkyOps, an aviation ground operations intelligence assistant.",
        ),
        ChatMessage(
            role="user",
            content="Confirm operational readiness for ground turnaround testing.",
        ),
    ]

    print("[REQUEST] Sending test message to adapter...")
    start_time = time.perf_counter()

    try:
        response = client.complete(messages, temperature=0.0)
        elapsed = round((time.perf_counter() - start_time) * 1000, 2)

        print("-" * 70)
        print("[SUCCESS] Completion received successfully!")
        print(f"Provider:      {response.provider}")
        print(f"Model:         {response.model}")
        print(f"Latency:       {elapsed} ms (Adapter report: {response.latency_ms} ms)")
        print(f"Finish Reason: {response.finish_reason}")
        print(f"Token Usage:   {response.usage}")
        print("-" * 70)
        print("Response Content:")
        print(response.content.strip())
        print("=" * 70)
        return 0

    except LLMError as err:
        print("-" * 70)
        print(f"[FAILED] LLM Client Error ({type(err).__name__}): {err.message}")
        if err.details:
            print(f"Details: {err.details}")
        print("=" * 70)
        return 1
    except Exception as exc:
        print("-" * 70)
        print(f"[FAILED] Unexpected Exception: {str(exc)}")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SkyOps LLM Smoke Test")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run smoke test using Mock client adapter (offline, zero cost)",
    )
    args = parser.parse_args()

    exit_code = run_smoke_test(use_mock=args.mock)
    sys.exit(exit_code)
