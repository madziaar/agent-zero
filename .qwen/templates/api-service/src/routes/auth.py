"""
Authentication routes for user registration, login, and token management.

Features:
- User registration with email verification
- JWT-based authentication
- Password reset functionality
- Token refresh
- Logout functionality
"""

from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_db
from ..config.settings import settings
from ..middleware.auth import (
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
)
from ..models.user import User

router = APIRouter()


# Pydantic models for request/response
class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user information in responses."""
    id: int
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_verified: bool
    created_at: str

    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Register a new user account.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        User: Created user information

    Raises:
        HTTPException: If user already exists
    """
    # Check if user already exists
    existing_user = await db.get(User, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    # Check if email already exists
    query = await db.execute(
        "SELECT * FROM users WHERE email = :email",
        {"email": user_data.email}
    )
    existing_email = query.first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_active=True,
        is_verified=False,
    )
    db_user.set_password(user_data.password)

    # Generate verification token
    verification_token = db_user.generate_verification_token()

    # Save to database
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # TODO: Send verification email here
    # await send_verification_email(db_user.email, verification_token)

    return db_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Authenticate user and return JWT tokens.

    Args:
        form_data: OAuth2 form data (username/password)
        db: Database session

    Returns:
        Dict with access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Get user from database
    query = await db.execute(
        "SELECT * FROM users WHERE username = :username OR email = :email",
        {"username": form_data.username, "email": form_data.username}
    )
    user = query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to User object
    db_user = User(**user._mapping)

    # Verify password
    if not db_user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    db_user.update_last_login()
    await db.commit()

    # Create tokens
    token_data = {"sub": str(db_user.id), "username": db_user.username}
    access_token = create_access_token(
        token_data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Refresh access token using refresh token.

    Args:
        refresh_data: Refresh token data
        db: Database session

    Returns:
        Dict with new access and refresh tokens

    Raises:
        HTTPException: If refresh token is invalid
    """
    from ..middleware.auth import decode_token

    # Decode refresh token
    payload = decode_token(refresh_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Get user from database
    db_user = await db.get(User, int(user_id))
    if not db_user or not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Create new tokens
    token_data = {"sub": str(db_user.id), "username": db_user.username}
    access_token = create_access_token(
        token_data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, str]:
    """
    Logout user (client-side token removal).

    Note: JWT tokens are stateless, so "logout" is handled client-side
    by removing the token. This endpoint can be used for server-side
    cleanup if needed.

    Args:
        current_user: Current authenticated user

    Returns:
        Dict with logout confirmation
    """
    # TODO: Add token to blacklist if using token blacklisting
    # TODO: Cleanup user sessions if needed

    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user information
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    first_name: str | None = None,
    last_name: str | None = None,
    preferred_model: str | None = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Update current user information.

    Args:
        first_name: New first name
        last_name: New last name
        preferred_model: New preferred AI model
        current_user: Current authenticated user
        db: Database session

    Returns:
        User: Updated user information
    """
    # Update user fields
    if first_name is not None:
        current_user.first_name = first_name
    if last_name is not None:
        current_user.last_name = last_name
    if preferred_model is not None:
        current_user.preferred_model = preferred_model

    current_user.touch()
    await db.commit()
    await db.refresh(current_user)

    return current_user


@router.post("/verify-email/{token}")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Verify user email address.

    Args:
        token: Email verification token
        db: Database session

    Returns:
        Dict with verification status

    Raises:
        HTTPException: If token is invalid
    """
    # Find user by verification token
    query = await db.execute(
        "SELECT * FROM users WHERE verification_token = :token",
        {"token": token}
    )
    user = query.first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )

    # Convert to User object and verify
    db_user = User(**user._mapping)
    db_user.verify_email()

    await db.commit()

    return {"message": "Email verified successfully"}