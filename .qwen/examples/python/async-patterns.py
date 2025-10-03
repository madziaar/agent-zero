"""
Qwen-Optimized Async Patterns for Python

This module demonstrates async patterns optimized for Qwen AI model
understanding. These patterns are designed to be:
- Easy for Qwen to generate correctly
- Performance-optimized for async workloads
- Following Python best practices
- Well-documented for context retention
"""

import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from contextlib import asynccontextmanager


@dataclass
class APIConfig:
    """Configuration for API connections - Qwen-optimized dataclass pattern."""
    base_url: str
    timeout: int = 30
    max_concurrent: int = 10
    retry_attempts: int = 3


class QwenOptimizedAPIClient:
    """
    Async API client optimized for Qwen model generation patterns.

    Key optimizations for Qwen:
    - Clear separation of concerns
    - Comprehensive error handling
    - Performance monitoring
    - Memory-efficient patterns
    """

    def __init__(self, config: APIConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_count = 0
        self.error_count = 0

        # Configure logging for Qwen context
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """Async context manager entry - Qwen-optimized pattern."""
        await self._initialize_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        await self._close_session()

    async def _initialize_session(self):
        """Initialize aiohttp session with optimal settings."""
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        # Qwen-optimized connector configuration
        connector = aiohttp.TCPConnector(
            limit=self.config.max_concurrent,
            limit_per_host=self.config.max_concurrent // 2,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )

        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                'User-Agent': 'Qwen-Optimized-Client/1.0',
                'Accept': 'application/json',
            }
        )

    async def _close_session(self):
        """Properly close session and cleanup resources."""
        if self.session:
            await self.session.close()
            self.session = None

    async def fetch_with_retry(self, url: str, **kwargs) -> Dict[str, Any]:
        """
        Fetch data with retry logic - Qwen-optimized error handling.

        Args:
            url: Target URL for the request
            **kwargs: Additional arguments for aiohttp request

        Returns:
            Response data as dictionary

        Raises:
            aiohttp.ClientError: After all retry attempts exhausted
        """
        last_exception = None

        for attempt in range(self.config.retry_attempts):
            try:
                self.request_count += 1

                if not self.session:
                    await self._initialize_session()

                async with self.session.get(url, **kwargs) as response:
                    response.raise_for_status()
                    data = await response.json()

                    self.logger.info(f"Successful request to {url}")
                    return data

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                self.error_count += 1

                if attempt < self.config.retry_attempts - 1:
                    # Exponential backoff - Qwen-optimized delay pattern
                    delay = (2 ** attempt) * 0.1
                    self.logger.warning(
                        f"Request failed (attempt {attempt + 1}), "
                        f"retrying in {delay}s: {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(
                        f"Request failed after {self.config.retry_attempts} "
                        f"attempts: {e}"
                    )

        # Re-raise the last exception if all retries failed
        if last_exception:
            raise last_exception
        else:
            raise aiohttp.ClientError("Unknown error occurred")


async def batch_process_optimized(
    items: List[Dict[str, Any]],
    processor_func: callable,
    batch_size: int = 10,
    max_concurrent: int = 5
) -> List[Dict[str, Any]]:
    """
    Process items in optimized batches - Qwen memory-efficient pattern.

    Args:
        items: List of items to process
        processor_func: Async function to process each item
        batch_size: Number of items per batch
        max_concurrent: Maximum concurrent batches

    Returns:
        List of processed results in original order
    """
    results = [None] * len(items)  # Pre-allocate for order preservation
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(batch_indices: List[int]):
        """Process a single batch of items."""
        async with semaphore:
            for idx in batch_indices:
                try:
                    # Qwen-optimized error isolation
                    results[idx] = await processor_func(items[idx])
                except Exception as e:
                    logging.error(f"Error processing item {idx}: {e}")
                    results[idx] = {"error": str(e)}

    # Create batch tasks - Qwen-optimized task grouping
    tasks = []
    for i in range(0, len(items), batch_size):
        batch_indices = list(range(i, min(i + batch_size, len(items))))
        task = asyncio.create_task(process_batch(batch_indices))
        tasks.append(task)

    # Wait for all batches to complete
    await asyncio.gather(*tasks)

    return results


@asynccontextmanager
async def managed_api_client(config: APIConfig):
    """
    Context manager for API client - Qwen-optimized resource management.

    Usage:
        async with managed_api_client(
            APIConfig("https://api.example.com")
        ) as client:
            data = await client.fetch_with_retry("/endpoint")
    """
    client = QwenOptimizedAPIClient(config)
    await client._initialize_session()

    try:
        yield client
    finally:
        await client._close_session()


# Example usage and testing
async def main():
    """Example demonstrating Qwen-optimized async patterns."""

    # Configuration optimized for Qwen understanding
    config = APIConfig(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=10,
        max_concurrent=5,
        retry_attempts=2
    )

    # Qwen-optimized processing pattern
    async def fetch_user(user_id: int) -> Dict[str, Any]:
        """Fetch user data - simple function for Qwen generation."""
        async with managed_api_client(config) as client:
            return await client.fetch_with_retry(f"/users/{user_id}")

    # Example items to process
    user_ids = [1, 2, 3, 4, 5]

    # Process users with Qwen-optimized batching
    users = await batch_process_optimized(
        items=user_ids,
        processor_func=lambda uid: fetch_user(uid),
        batch_size=2,
        max_concurrent=2
    )

    # Qwen-optimized result processing
    for i, user in enumerate(users):
        if "error" not in user:
            print(f"User {i+1}: {user.get('name', 'Unknown')}")
        else:
            print(f"User {i+1}: Error - {user['error']}")


if __name__ == "__main__":
    # Run example - Qwen-optimized entry point
    asyncio.run(main())
