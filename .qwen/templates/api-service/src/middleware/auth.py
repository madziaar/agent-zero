"""
Authentication middleware and utilities for JWT token handling.

Features:
- JWT token validation and decoding
- User authentication dependencies
- Role-based access control
- Password verification utilities
- Token generation and management
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_db
from ..config.settings import settings
from ..models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Get the current authenticated user from JWT token.

    Args:
        credentials: Bearer token credentials
        db: Database session

    Returns:
        User or None if not authenticated

    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not credentials:
        return None

    token = credentials.credentials

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extract user information
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            return None

        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            return None

    except JWTError:
        return None

    # Get user from database
    result = await db.get(User, int(user_id))
    if not result:
        return None

    return result


async def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Get the current authenticated and active user.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        User: Active authenticated user

    Raises:
        HTTPException: If user is not authenticated or inactive
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get the current authenticated, active, and verified user.

    Args:
        current_user: User from get_current_active_user dependency

    Returns:
        User: Verified authenticated user

    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )

    return current_user


async def require_superuser(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Require the current user to be a superuser.

    Args:
        current_user: User from get_current_verified_user dependency

    Returns:
        User: Superuser

    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storage.

    Args:
        password: The plain text password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode in token
        expires_delta: Token expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Payload data to encode in token

    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)  # Refresh tokens last 7 days

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        dict or None: Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            return None

        return payload

    except JWTError:
        return None


class AuthMiddleware:
    """
    Middleware for handling authentication across requests.

    This middleware can be used to:
    - Extract user information from tokens
    - Set user context for logging
    - Handle authentication errors
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        Process the ASGI call and handle authentication.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # For HTTP requests, authentication is handled by dependencies
        # This middleware mainly serves as a placeholder for future enhancements
        await self.app(scope, receive, send)


# Optional: Request-scoped user storage
class UserContext:
    """
    Context manager for storing user information in request state.
    """

    def __init__(self, request: Request, user: Optional[User]):
        """
        Initialize user context.

        Args:
            request: The HTTP request
            user: The authenticated user (if any)
        """
        self.request = request
        self.user = user

    async def __aenter__(self):
        """Enter the context and set user in request state."""
        self.request.state.user = self.user
        if self.user:
            self.request.state.user_id = self.user.id
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and clean up request state."""
        if hasattr(self.request.state, 'user'):
            delattr(self.request.state, 'user')
        if hasattr(self.request.state, 'user_id'):
            delattr(self.request.state, 'user_id')