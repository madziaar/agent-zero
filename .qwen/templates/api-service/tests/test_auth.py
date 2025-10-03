"""
Tests for authentication routes and functionality.

Tests:
- User registration
- User login and token generation
- Token refresh
- Password verification
- Email verification
- Authentication middleware
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


class TestUserRegistration:
    """Test user registration functionality."""

    def test_register_user_success(self, test_client: TestClient, db_session: AsyncSession):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepassword123",
            "first_name": "New",
            "last_name": "User"
        }

        response = test_client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["first_name"] == user_data["first_name"]
        assert data["is_active"] is True
        assert data["is_verified"] is False  # Should not be verified initially

    def test_register_user_duplicate_email(self, test_client: TestClient, test_user: User):
        """Test registration with duplicate email."""
        user_data = {
            "email": test_user.email,  # Use existing email
            "username": "differentuser",
            "password": "password123"
        }

        response = test_client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    def test_register_user_duplicate_username(self, test_client: TestClient, test_user: User):
        """Test registration with duplicate username."""
        user_data = {
            "email": "different@example.com",
            "username": test_user.username,  # Use existing username
            "password": "password123"
        }

        response = test_client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already taken" in response.json()["detail"]

    def test_register_user_invalid_email(self, test_client: TestClient):
        """Test registration with invalid email."""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "password123"
        }

        response = test_client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_weak_password(self, test_client: TestClient):
        """Test registration with weak password."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "123"  # Too short
        }

        response = test_client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Test user login functionality."""

    def test_login_success(self, test_client: TestClient, test_user: User):
        """Test successful user login."""
        login_data = {
            "username": test_user.username,
            "password": "testpassword123"
        }

        response = test_client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_wrong_password(self, test_client: TestClient, test_user: User):
        """Test login with wrong password."""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }

        response = test_client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, test_client: TestClient):
        """Test login with nonexistent user."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }

        response = test_client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user(self, test_client: TestClient, db_session: AsyncSession):
        """Test login with inactive user."""
        # Create inactive user
        inactive_user = User(
            email="inactive@example.com",
            username="inactiveuser",
            is_active=False,
            is_verified=True
        )
        inactive_user.set_password("password123")

        db_session.add(inactive_user)
        db_session.commit()
        db_session.refresh(inactive_user)

        login_data = {
            "username": inactive_user.username,
            "password": "password123"
        }

        response = test_client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenRefresh:
    """Test token refresh functionality."""

    def test_refresh_token_success(self, test_client: TestClient, test_user: User):
        """Test successful token refresh."""
        # First login to get refresh token
        login_data = {
            "username": test_user.username,
            "password": "testpassword123"
        }

        login_response = test_client.post("/api/v1/auth/login", data=login_data)
        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        refresh_data = {"refresh_token": refresh_token}
        response = test_client.post("/api/v1/auth/refresh", json=refresh_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_invalid_token(self, test_client: TestClient):
        """Test refresh with invalid token."""
        refresh_data = {"refresh_token": "invalid_token"}

        response = test_client.post("/api/v1/auth/refresh", json=refresh_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCurrentUser:
    """Test current user endpoints."""

    def test_get_current_user_success(self, test_client: TestClient, test_user_token: str):
        """Test getting current user information."""
        headers = {"Authorization": f"Bearer {test_user_token}"}

        response = test_client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True

    def test_get_current_user_unauthorized(self, test_client: TestClient):
        """Test getting current user without authentication."""
        response = test_client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_current_user(self, test_client: TestClient, test_user_token: str):
        """Test updating current user information."""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }

        response = test_client.put("/api/v1/auth/me", json=update_data, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"


class TestEmailVerification:
    """Test email verification functionality."""

    def test_verify_email_success(self, test_client: TestClient, db_session: AsyncSession):
        """Test successful email verification."""
        # Create user with verification token
        user = User(
            email="verify@example.com",
            username="verifyuser",
            is_verified=False
        )
        user.set_password("password123")
        verification_token = user.generate_verification_token()

        db_session.add(user)
        db_session.commit()

        # Verify email
        response = test_client.post(f"/api/v1/auth/verify-email/{verification_token}")

        assert response.status_code == status.HTTP_200_OK
        assert "verified successfully" in response.json()["message"]

        # Check user is now verified
        db_session.refresh(user)
        assert user.is_verified is True
        assert user.verification_token is None

    def test_verify_email_invalid_token(self, test_client: TestClient):
        """Test email verification with invalid token."""
        response = test_client.post("/api/v1/auth/verify-email/invalid_token")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid verification token" in response.json()["detail"]


class TestAuthenticationMiddleware:
    """Test authentication middleware functionality."""

    def test_protected_route_with_valid_token(self, test_client: TestClient, test_user_token: str):
        """Test accessing protected route with valid token."""
        headers = {"Authorization": f"Bearer {test_user_token}"}

        response = test_client.get("/api/v1/users/me", headers=headers)

        assert response.status_code == status.HTTP_200_OK

    def test_protected_route_without_token(self, test_client: TestClient):
        """Test accessing protected route without token."""
        response = test_client.get("/api/v1/users/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_route_with_invalid_token(self, test_client: TestClient):
        """Test accessing protected route with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}

        response = test_client.get("/api/v1/users/me", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestPasswordSecurity:
    """Test password security functionality."""

    def test_password_hashing(self, db_session: AsyncSession):
        """Test password hashing and verification."""
        user = User(
            email="hash@example.com",
            username="hashtest"
        )

        plain_password = "securepassword123"
        user.set_password(plain_password)

        # Test correct password
        assert user.verify_password(plain_password) is True

        # Test incorrect password
        assert user.verify_password("wrongpassword") is False

        # Test empty password
        assert user.verify_password("") is False

    def test_password_strength_requirements(self):
        """Test password strength validation."""
        from ..src.services.user_service import UserService

        # Test weak passwords
        weak_passwords = ["123", "abc", "short"]

        for password in weak_passwords:
            with pytest.raises(ValueError, match="at least 8 characters"):
                # This would be caught during user creation
                pass


class TestTokenGeneration:
    """Test JWT token generation and validation."""

    def test_access_token_creation(self, test_user: User):
        """Test access token creation."""
        from ..src.middleware.auth import create_access_token
        from datetime import timedelta

        token_data = {"sub": str(test_user.id), "username": test_user.username}
        token = create_access_token(token_data, expires_delta=timedelta(minutes=30))

        assert isinstance(token, str)
        assert len(token) > 0

        # Token should be decodable
        from ..src.middleware.auth import decode_token
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded["sub"] == str(test_user.id)
        assert decoded["username"] == test_user.username
        assert decoded["type"] == "access"

    def test_refresh_token_creation(self, test_user: User):
        """Test refresh token creation."""
        from ..src.middleware.auth import create_refresh_token

        token_data = {"sub": str(test_user.id), "username": test_user.username}
        token = create_refresh_token(token_data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Token should be decodable
        from ..src.middleware.auth import decode_token
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded["sub"] == str(test_user.id)
        assert decoded["type"] == "refresh"

    def test_token_expiration(self, test_user: User):
        """Test token expiration."""
        from ..src.middleware.auth import create_access_token, decode_token
        from datetime import timedelta

        # Create token that expires immediately
        token_data = {"sub": str(test_user.id), "username": test_user.username}
        token = create_access_token(token_data, expires_delta=timedelta(seconds=0))

        # Token should be invalid immediately
        decoded = decode_token(token)
        assert decoded is None