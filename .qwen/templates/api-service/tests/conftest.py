"""
Pytest configuration and fixtures for API service testing.

Features:
- Test database setup and teardown
- Test client configuration
- Authentication fixtures
- Mock services for external APIs
- Test data factories
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..main import create_application
from ..src.config.database import Base
from ..src.config.settings import settings
from ..src.models.user import User
from ..src.services.qwen_service import QwenService


# Test database configuration
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,  # Disable SQL echo for tests
)

# Create test session factory
TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_test_database():
    """Create test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def teardown_test_database():
    """Drop test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_test_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test.

    This fixture:
    - Creates a new session for each test
    - Rolls back transactions after each test
    - Closes the session properly
    """
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """
    Create FastAPI test client.

    This fixture provides a TestClient instance for testing API endpoints
    without running a live server.
    """
    app = create_application()

    # Override settings for testing
    app.dependency_overrides = {}

    with TestClient(app) as client:
        yield client


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create async HTTP client for testing.

    Useful for testing async endpoints and WebSocket connections.
    """
    async with AsyncClient() as client:
        yield client


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """
    Create a test user for authentication testing.

    Returns:
        User: Test user instance
    """
    user = User(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_verified=True,
    )
    user.set_password("testpassword123")

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def test_superuser(db_session: AsyncSession) -> User:
    """
    Create a test superuser for admin testing.

    Returns:
        User: Test superuser instance
    """
    user = User(
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="User",
        is_active=True,
        is_verified=True,
        is_superuser=True,
    )
    user.set_password("adminpassword123")

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def test_user_token(test_user: User) -> str:
    """
    Create JWT token for test user.

    Args:
        test_user: Test user instance

    Returns:
        str: JWT access token
    """
    from ..src.middleware.auth import create_access_token
    from datetime import timedelta

    token_data = {"sub": str(test_user.id), "username": test_user.username}
    return create_access_token(
        token_data,
        expires_delta=timedelta(minutes=30)
    )


@pytest.fixture
async def test_superuser_token(test_superuser: User) -> str:
    """
    Create JWT token for test superuser.

    Args:
        test_superuser: Test superuser instance

    Returns:
        str: JWT access token
    """
    from ..src.middleware.auth import create_access_token
    from datetime import timedelta

    token_data = {"sub": str(test_superuser.id), "username": test_superuser.username}
    return create_access_token(
        token_data,
        expires_delta=timedelta(minutes=30)
    )


@pytest.fixture
def qwen_service() -> QwenService:
    """
    Create Qwen service instance for testing.

    Returns:
        QwenService: Service instance with test configuration
    """
    return QwenService()


@pytest.fixture
def mock_qwen_response():
    """
    Mock Qwen API response for testing.

    Returns:
        dict: Mock API response
    """
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a test response from Qwen AI.",
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 15,
            "total_tokens": 25
        },
        "model": "qwen-turbo"
    }


@pytest.fixture
def sample_chat_messages():
    """
    Sample chat messages for testing.

    Returns:
        list: List of chat message dictionaries
    """
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]


@pytest.fixture
def test_headers(test_user_token: str) -> dict:
    """
    Create test headers with authentication.

    Args:
        test_user_token: JWT token for test user

    Returns:
        dict: Headers dictionary with authorization
    """
    return {
        "Authorization": f"Bearer {test_user_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def test_admin_headers(test_superuser_token: str) -> dict:
    """
    Create test admin headers with authentication.

    Args:
        test_superuser_token: JWT token for test superuser

    Returns:
        dict: Headers dictionary with admin authorization
    """
    return {
        "Authorization": f"Bearer {test_superuser_token}",
        "Content-Type": "application/json"
    }


# Test configuration
def pytest_configure(config):
    """
    Configure pytest settings.

    Args:
        config: Pytest config object
    """
    # Add custom markers
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers.

    Args:
        config: Pytest config
        items: Test items
    """
    # Add markers based on test file names
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)


# Environment setup for testing
@pytest.fixture(scope="session", autouse=True)
def set_test_environment():
    """
    Set test environment variables.

    This fixture runs automatically for all tests.
    """
    # Override settings for testing
    settings.ENVIRONMENT = "testing"
    settings.DEBUG = True
    settings.DATABASE_URL = TEST_DATABASE_URL
    settings.REDIS_URL = None  # Disable Redis for testing
    settings.QWEN_API_KEY = "test-api-key"  # Mock API key

    yield

    # Cleanup after tests
    settings.ENVIRONMENT = "development"