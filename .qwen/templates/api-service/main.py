"""
Qwen API Service Template - Main Application Entry Point

A modern, production-ready FastAPI application template with:
- Authentication and authorization
- Database integration (SQLAlchemy + PostgreSQL)
- Structured logging and monitoring
- Rate limiting and CORS
- Health checks and metrics
- Qwen AI integration patterns
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog

from src.config.database import engine, Base, get_db
from src.config.settings import settings
from src.middleware.logging import LoggingMiddleware
from src.middleware.rate_limiting import RateLimitMiddleware
from src.routes import health, auth, users, qwen_integration

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown events.
    """
    logger.info("Starting Qwen API Service Template")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created/verified")

    # Startup tasks
    logger.info(f"Server starting on {settings.HOST}:{settings.PORT}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    yield

    # Shutdown tasks
    logger.info("Shutting down Qwen API Service Template")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A modern API service template with Qwen AI integration patterns",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(
            "Unhandled exception",
            path=request.url.path,
            method=request.method,
            error=str(exc),
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    # Security middleware
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

    # CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)

    return app


# Create the FastAPI application instance
app = create_application()


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - returns basic API information.
    """
    return {
        "message": "Welcome to Qwen API Service Template",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring systems.
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# Include routers
app.include_router(
    health.router,
    prefix=f"{settings.API_V1_PREFIX}/health",
    tags=["health"],
)
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["authentication"],
)
app.include_router(
    users.router,
    prefix=f"{settings.API_V1_PREFIX}/users",
    tags=["users"],
)
app.include_router(
    qwen_integration.router,
    prefix=f"{settings.API_V1_PREFIX}/qwen",
    tags=["qwen-integration"],
)


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server with uvicorn on {settings.HOST}:{settings.PORT}")

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )