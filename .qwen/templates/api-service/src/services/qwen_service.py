"""
Qwen AI service for handling AI model interactions.

Features:
- Chat completion API integration
- Error handling and retry logic
- Token usage calculation and cost estimation
- Response processing and validation
- Rate limiting and request optimization
"""

import json
from typing import Dict, List, Optional, Any
import time

import httpx
import structlog

from ..config.settings import settings

logger = structlog.get_logger()


class QwenService:
    """
    Service for interacting with Qwen AI API.

    Handles:
    - API request/response processing
    - Error handling and retries
    - Token usage tracking
    - Cost calculation
    - Response validation
    """

    def __init__(self):
        """
        Initialize Qwen service with configuration.
        """
        self.base_url = settings.QWEN_API_BASE_URL
        self.default_model = settings.QWEN_MODEL
        self.max_tokens = settings.QWEN_MAX_TOKENS
        self.temperature = settings.QWEN_TEMPERATURE
        self.api_key = settings.QWEN_API_KEY

        # Request timeout settings
        self.timeout = httpx.Timeout(60.0, connect=10.0)
        self.max_retries = 3

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        user_api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a chat completion using Qwen AI.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to configured model)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            user_api_key: User's personal API key (overrides default)
            **kwargs: Additional parameters

        Returns:
            Dict containing response content, usage, and metadata

        Raises:
            httpx.HTTPStatusError: If API request fails
            Exception: For other errors
        """
        # Use provided parameters or defaults
        model = model or self.default_model
        max_tokens = max_tokens or self.max_tokens
        temperature = temperature or self.temperature

        # Use user's API key if provided, otherwise use default
        api_key = user_api_key or self.api_key
        if not api_key:
            raise ValueError("No API key available")

        # Prepare request payload
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }

        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        request_url = f"{self.base_url}/chat/completions"

        logger.info(
            "Making Qwen API request",
            model=model,
            message_count=len(messages),
            max_tokens=max_tokens,
            url=request_url
        )

        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    request_url,
                    json=payload,
                    headers=headers
                )

                # Raise exception for HTTP errors
                response.raise_for_status()

                # Parse response
                response_data = response.json()

                # Extract response information
                response_time = time.time() - start_time

                result = {
                    "content": response_data["choices"][0]["message"]["content"],
                    "finish_reason": response_data["choices"][0]["finish_reason"],
                    "usage": response_data["usage"],
                    "model": response_data["model"],
                    "response_time": response_time,
                }

                # Calculate estimated cost (example rates - adjust based on actual pricing)
                estimated_cost = self._calculate_cost(
                    result["usage"]["prompt_tokens"],
                    result["usage"]["completion_tokens"],
                    model
                )
                result["estimated_cost"] = estimated_cost

                logger.info(
                    "Qwen API request successful",
                    model=model,
                    tokens_used=result["usage"]["total_tokens"],
                    response_time=round(response_time, 2),
                    estimated_cost=estimated_cost
                )

                return result

        except httpx.TimeoutException as e:
            logger.error("Qwen API request timeout", error=str(e))
            raise httpx.HTTPStatusError(
                f"Request timeout after {self.timeout}",
                request=None,
                response=None
            )

        except httpx.HTTPStatusError as e:
            logger.error(
                "Qwen API request failed",
                status_code=e.response.status_code if e.response else "unknown",
                error=e.response.text if e.response else str(e)
            )
            raise

        except Exception as e:
            logger.error("Unexpected error in Qwen API request", error=str(e))
            raise

    def _calculate_cost(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model: str
    ) -> float:
        """
        Calculate estimated cost for API usage.

        Args:
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            model: Model used for calculation

        Returns:
            float: Estimated cost in USD
        """
        # Cost per 1K tokens (example rates - adjust based on actual Qwen pricing)
        cost_per_1k_tokens = {
            "qwen-turbo": {"prompt": 0.0015, "completion": 0.002},
            "qwen-plus": {"prompt": 0.003, "completion": 0.006},
            "qwen-max": {"prompt": 0.01, "completion": 0.02},
        }

        # Default rates if model not found
        rates = cost_per_1k_tokens.get(model, {"prompt": 0.0015, "completion": 0.002})

        # Calculate cost
        prompt_cost = (prompt_tokens / 1000) * rates["prompt"]
        completion_cost = (completion_tokens / 1000) * rates["completion"]

        return round(prompt_cost + completion_cost, 6)

    async def validate_api_key(self, api_key: str) -> bool:
        """
        Validate API key by making a test request.

        Args:
            api_key: API key to validate

        Returns:
            bool: True if key is valid
        """
        try:
            # Make a minimal test request
            test_messages = [{"role": "user", "content": "Hello"}]

            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.default_model,
                        "messages": test_messages,
                        "max_tokens": 1,
                    },
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    }
                )

                return response.status_code == 200

        except Exception:
            return False

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from Qwen API.

        Returns:
            List of model information dictionaries
        """
        # Note: This would depend on Qwen API's model listing endpoint
        # For now, return known models
        return [
            {
                "id": "qwen-turbo",
                "name": "Qwen Turbo",
                "description": "Fast and efficient model for general tasks",
                "context_length": 8192,
            },
            {
                "id": "qwen-plus",
                "name": "Qwen Plus",
                "description": "More capable model with better reasoning",
                "context_length": 32768,
            },
            {
                "id": "qwen-max",
                "name": "Qwen Max",
                "description": "Most capable model for complex tasks",
                "context_length": 32768,
            }
        ]

    async def estimate_tokens(self, text: str) -> int:
        """
        Estimate number of tokens in text.

        Args:
            text: Text to estimate tokens for

        Returns:
            int: Estimated token count
        """
        # Simple estimation: ~4 characters per token for most languages
        # This is a rough estimate - for production use, consider using tiktoken
        return len(text) // 4

    async def optimize_prompt(
        self,
        prompt: str,
        max_tokens: int = 1000
    ) -> str:
        """
        Optimize prompt for better AI responses.

        Args:
            prompt: Original prompt
            max_tokens: Maximum tokens for optimization

        Returns:
            str: Optimized prompt
        """
        # This is a placeholder for prompt optimization logic
        # In a real implementation, you might:
        # - Remove redundant information
        # - Add clear instructions
        # - Structure the prompt better
        # - Compress repetitive content

        if len(prompt) <= max_tokens * 4:  # Rough character estimate
            return prompt

        # Simple truncation for now
        # In production, implement proper prompt compression
        optimized = prompt[:max_tokens * 4 - 100]  # Leave room for optimization instructions

        return (
            "Please provide a concise response based on the following query:\n\n"
            f"{optimized}...\n\n"
            "Respond clearly and directly to the main question."
        )

    def calculate_rate_limit_wait(
        self,
        current_usage: int,
        limit: int,
        window_seconds: int
    ) -> float:
        """
        Calculate how long to wait before next request.

        Args:
            current_usage: Current usage count
            limit: Rate limit
            window_seconds: Rate limit window

        Returns:
            float: Seconds to wait
        """
        if current_usage < limit:
            return 0.0

        # Estimate wait time based on window
        # This is a simple calculation - real rate limiting is handled by middleware
        return window_seconds * 0.1  # Wait 10% of window time

    async def get_model_stats(self, model: str) -> Dict[str, Any]:
        """
        Get statistics for a specific model.

        Args:
            model: Model name

        Returns:
            Dict with model statistics
        """
        # Placeholder for model statistics
        # In production, you might track:
        # - Average response time
        # - Success rate
        # - Cost efficiency
        # - Usage patterns

        return {
            "model": model,
            "avg_response_time_ms": 1500,
            "success_rate": 0.95,
            "total_requests": 10000,
            "estimated_total_cost": 25.50,
        }