"""
User model for authentication and user management.

Features:
- Password hashing with bcrypt
- JWT token support
- Role-based access control
- Email verification
- Account status management
"""

from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """
    User model for authentication and user management.
    """
    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # Authentication fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # User profile
    first_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # Account verification
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    verification_token: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    # Account status
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Qwen AI preferences
    qwen_api_key: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    preferred_model: Mapped[str] = mapped_column(
        String(100),
        default="qwen-turbo",
        nullable=False
    )

    # Relationships (if needed)
    # qwen_sessions: Mapped[List["QwenSession"]] = relationship(
    #     "QwenSession",
    #     back_populates="user",
    #     cascade="all, delete-orphan"
    # )

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.is_active and self.is_verified

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify a password against the hashed password.

        Args:
            plain_password: The plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password: str) -> None:
        """
        Hash and set the user's password.

        Args:
            plain_password: The plain text password to hash
        """
        self.hashed_password = pwd_context.hash(plain_password)

    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()

    def generate_verification_token(self) -> str:
        """
        Generate a verification token for email verification.

        Returns:
            str: Generated verification token
        """
        import secrets
        token = secrets.token_urlsafe(32)
        self.verification_token = token
        return token

    def verify_email(self) -> None:
        """Mark the user's email as verified."""
        self.is_verified = True
        self.verification_token = None

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    def __repr__(self) -> str:
        """String representation of the user."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"