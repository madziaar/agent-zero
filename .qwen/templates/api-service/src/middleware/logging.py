"""
Structured logging middleware for request/response logging.

Features:
- Request/response logging with timing
- Structured logging with context
- Request ID tracking
- Error logging with stack traces
- Performance monitoring
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured logging of HTTP requests and responses.

    Logs:
    - Request start with method, URL, client info
    - Request completion with status code, duration
    - Errors with stack traces
    - Request IDs for tracing
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log relevant information.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware in the chain

        Returns:
            Response: The HTTP response
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Add request ID to headers for tracing
        request.state.request_id = request_id

        # Get client information
        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else 0

        # Log request start
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            path=request.url.path,
            query_params=dict(request.query_params),
            client_host=client_host,
            client_port=client_port,
            user_agent=request.headers.get("user-agent"),
        )

        # Record start time
        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000

            # Log successful request
            logger.info(
                "Request completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
                response_size=self._get_response_size(response),
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:
            # Calculate duration for failed request
            duration_ms = (time.time() - start_time) * 1000

            # Log error with stack trace
            logger.error(
                "Request failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error=str(exc),
                duration_ms=round(duration_ms, 2),
                exc_info=True,
            )

            # Add request ID to error response if possible
            if hasattr(request.state, 'request_id'):
                # We'll handle this in the global exception handler
                pass

            raise

    def _get_response_size(self, response: Response) -> int:
        """
        Get the size of the response body.

        Args:
            response: The HTTP response

        Returns:
            int: Size of response body in bytes, or 0 if unknown
        """
        try:
            # Try to get content-length header
            content_length = response.headers.get("content-length")
            if content_length:
                return int(content_length)

            # If it's a JSON response, we could estimate size
            # For now, return 0 as we don't want to consume the response body
            return 0

        except (ValueError, TypeError):
            return 0


class RequestContextMiddleware:
    """
    Middleware to add request context to the logging context.

    This allows all log entries within a request to include
    request-specific information like request_id, user_id, etc.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        Process the ASGI call and add request context.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Add request context to structlog context
        request_id = str(uuid.uuid4())

        # Bind request context to logger
        with structlog.contextvars.merge_contextvars(
            request_id=request_id,
            path=scope.get("path", ""),
            method=scope.get("method", ""),
        ):
            await self.app(scope, receive, send)