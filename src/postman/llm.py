"""LLM integration module for OpenRouter API."""

import os
from typing import AsyncIterator, Optional


class LLMError(Exception):
    """Custom exception for LLM-related errors."""


from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from postman.config import config


class LLMClient:
    """Client for OpenRouter API using LangChain."""

    def __init__(self, model: Optional[str] = None):
        """Initialize LLM client with OpenRouter configuration."""
        self.model = model or config.model
        self.api_key = config.api_key

        # OpenRouter uses OpenAI-compatible API
        self.client = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            streaming=True,
        )

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def generate_stream(
        self, system_prompt: str, user_input: str
    ) -> AsyncIterator[str]:
        """Generate content with streaming response."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input),
        ]

        try:
            async for chunk in self.client.astream(messages):
                if chunk.content:
                    yield str(chunk.content)
        except Exception as e:
            # Convert to LLMError for consistent error handling
            raise LLMError(f"Failed to generate content: {e}") from e

    async def generate(
        self, system_prompt: str, user_input: str, max_sentences: int = 3
    ) -> str:
        """Generate content without streaming."""
        full_prompt = (
            f"{system_prompt}\n\nGenerate a post in exactly {max_sentences} sentences."
        )
        messages = [
            SystemMessage(content=full_prompt),
            HumanMessage(content=user_input),
        ]

        response = await self.client.ainvoke(messages)
        return str(response.content)
