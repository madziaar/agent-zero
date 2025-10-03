"""
Database configuration and session management for Qwen API Service Template.

Features:
- Async SQLAlchemy engine with connection pooling
- Database session management
- Migration support with Alembic
- Health check utilities
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import StaticPool

from .settings import settings

# Create async engine with proper configuration
if settings.ENVIRONMENT == "testing":
    # Use SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG,
    )
else:
    # Use PostgreSQL for development and production
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )

# Create async session factory
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Provides common functionality and configurations for all models.
    """
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.

    Yields:
        AsyncSession: Database session for the request

    Usage:
        @app.get("/items/")
        async def read_items(db: AsyncSession = Depends(get_db)):
            # Use db session
            pass
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> bool:
    """
    Check if database connection is healthy.

    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False


async def create_tables() -> None:
    """
    Create all database tables.

    Should be called during application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """
    Drop all database tables.

    WARNING: This will destroy all data. Use with caution.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)