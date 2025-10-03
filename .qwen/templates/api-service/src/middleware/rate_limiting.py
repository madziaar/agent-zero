"""
Rate limiting middleware for API protection.

Features:
- Redis-based rate limiting for distributed systems
- Multiple rate limiting strategies
- Configurable limits per endpoint
- User-specific and IP-based limiting
- Sliding window rate limiting
"""

import time
from typing import Optional, Tuple

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis
import structlog

from ..config.settings import settings

logger = structlog.get_logger()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis for storage.

    Supports:
    - Per-IP rate limiting
    - Per-user rate limiting (if authenticated)
    - Endpoint-specific limits
    - Sliding window algorithm
    """

    def __init__(self, app, redis_client: Optional[redis.Redis] = None):
        """
        Initialize rate limiting middleware.

        Args:
            app: The FastAPI application
            redis_client: Redis client instance (optional)
        """
        super().__init__(app)
        self.redis_client = redis_client or self._create_redis_client()

    def _create_redis_client(self) -> Optional[redis.Redis]:
        """
        Create Redis client from settings.

        Returns:
            Redis client instance or None if Redis is not configured
        """
        if not settings.REDIS_URL:
            logger.warning("Redis not configured, rate limiting disabled")
            return None

        try:
            return redis.from_url(settings.REDIS_URL)
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            return None

    def _get_client_identifier(self, request: Request) -> str:
        """
        Get unique identifier for the client.

        Args:
            request: The HTTP request

        Returns:
            str: Client identifier (IP or user ID)
        """
        # Try to get user ID from request state (set by auth middleware)
        if hasattr(request.state, 'user') and request.state.user:
            return f"user:{request.state.user.id}"

        # Fall back to IP address
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    def _get_endpoint_limit(self, path: str) -> Tuple[int, int]:
        """
        Get rate limit for specific endpoint.

        Args:
            path: Request path

        Returns:
            Tuple of (requests_per_window, window_seconds)
        """
        # Define endpoint-specific limits
        endpoint_limits = {
            "/api/v1/auth/login": (5, 60),  # 5 login attempts per minute
            "/api/v1/auth/register": (3, 300),  # 3 registrations per 5 minutes
            "/api/v1/qwen/chat": (50, 60),  # 50 AI requests per minute
            "/api/v1/users/me": (100, 60),  # 100 profile requests per minute
        }

        # Check for exact match first
        if path in endpoint_limits:
            return endpoint_limits[path]

        # Check for path prefix matches
        for endpoint, limit in endpoint_limits.items():
            if path.startswith(endpoint.rsplit('/', 1)[0]):
                return limit

        # Default rate limit
        return (settings.RATE_LIMIT_REQUESTS, settings.RATE_LIMIT_WINDOW)

    def _check_rate_limit(
        self,
        client_id: str,
        endpoint: str,
        limit: int,
        window: int
    ) -> Tuple[bool, int, int]:
        """
        Check if request is within rate limit.

        Args:
            client_id: Unique client identifier
            endpoint: Request endpoint
            limit: Maximum requests allowed
            window: Time window in seconds

        Returns:
            Tuple of (allowed, current_count, reset_time)
        """
        if not self.redis_client:
            # No Redis, allow all requests
            return True, 0, 0

        try:
            # Create Redis key for this client and endpoint
            key = f"rate_limit:{client_id}:{endpoint}"

            # Get current time
            now = int(time.time())

            # Clean old entries (sliding window)
            self.redis_client.zremrangebyscore(key, 0, now - window)

            # Count current requests in window
            current = self.redis_client.zcard(key)

            if current >= limit:
                # Rate limit exceeded
                # Get reset time (time of oldest request + window)
                oldest = self.redis_client.zrange(key, 0, 0, withscores=True)
                reset_time = int(oldest[0][1]) + window if oldest else now + window

                return False, current, reset_time

            # Add current request to window
            self.redis_client.zadd(key, {now: now})

            # Set key expiry
            self.redis_client.expire(key, window)

            return True, current + 1, 0

        except Exception as e:
            logger.error("Rate limit check failed", error=str(e))
            # Fail open - allow request if Redis fails
            return True, 0, 0

    async def dispatch(self, request: Request, call_next):
        """
        Check rate limit before processing request.

        Args:
            request: The HTTP request
            call_next: The next middleware in the chain

        Returns:
            Response or rate limit error
        """
        # Get client identifier
        client_id = self._get_client_identifier(request)

        # Get endpoint rate limit
        endpoint = request.url.path
        limit, window = self._get_endpoint_limit(endpoint)

        # Check rate limit
        allowed, current, reset_time = self._check_rate_limit(
            client_id, endpoint, limit, window
        )

        if not allowed:
            logger.warning(
                "Rate limit exceeded",
                client_id=client_id,
                endpoint=endpoint,
                limit=limit,
                current=current,
                reset_time=reset_time,
            )

            # Add rate limit headers
            response = JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
            )
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(reset_time)
            response.headers["Retry-After"] = str(window)

            return response

        # Process request
        response = await call_next(request)

        # Add rate limit headers to successful responses
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current))

        return response


class RateLimitExceeded(HTTPException):
    """
    Exception raised when rate limit is exceeded.
    """

    def __init__(self, limit: int, window: int, reset_time: int):
        """
        Initialize rate limit exception.

        Args:
            limit: Maximum requests allowed
            window: Time window in seconds
            reset_time: Unix timestamp when limit resets
        """
        self.limit = limit
        self.window = window
        self.reset_time = reset_time

        detail = f"Rate limit exceeded. Maximum {limit} requests per {window} seconds."
        super().__init__(
            status_code=429,
            detail=detail,
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Reset": str(reset_time),
                "Retry-After": str(window),
            }
        )