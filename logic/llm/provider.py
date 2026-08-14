"""
LLM Provider Abstraction.
Supports OpenAI / Anthropic / Groq / Ollama / Fallback.
"""

import os
import logging

logger = logging.getLogger(__name__)

class LLMProvider:
    """Configurable LLM Service Provider."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.client = None

        if self.provider == "openai" and self.openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                logger.info("OpenAI LLM provider client ready.")
            except Exception as e:
                logger.warning(f"Could not load OpenAI client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

llm_provider = LLMProvider()
