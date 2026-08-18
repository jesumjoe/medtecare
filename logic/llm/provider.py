"""
LLM Provider Abstraction.
Supports Live OpenAI, Live Groq, and Fallback modes.
"""

import os
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

logger = logging.getLogger(__name__)

class LLMProvider:
    """Configurable Live LLM Service Provider."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower() 
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.groq_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = None

        if self.provider == "groq" or (self.groq_key and not self.openai_key):
            try:
                from openai import OpenAI
                self.groq_model = os.getenv("LLM_MODEL") or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
                self.client = OpenAI(
                    api_key=self.groq_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                self.provider = "groq"
                self.model = self.groq_model
                logger.info(f"Groq Live LLM client initialized with model '{self.model}'.")
            except Exception as e:
                logger.warning(f"Could not load Groq client: {e}")

        elif self.openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                self.provider = "openai"
                logger.info(f"OpenAI Live LLM client initialized with model '{self.model}'.")
            except Exception as e:
                logger.warning(f"Could not load OpenAI client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

llm_provider = LLMProvider()
