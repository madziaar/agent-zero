"""
User service for business logic related to user management.

Features:
- User creation and validation
- Password management
- Email verification workflows
- User activity tracking
- Account security features
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
import structlog

from ..config.settings import settings
from ..models.user import User

logger = structlog.get_logger()


class UserService:
    """
    Service for user-related business logic.

    Handles:
    - User creation and validation
    - Authentication workflows
    - Account management
    - Security features
    """

    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_verified: bool = False
    ) -> User:
        """
        Create a new user with validation.

        Args:
            db: Database session
            email: User email address
            username: Unique username
            password: Plain text password
            first_name: Optional first name
            last_name: Optional last name
            is_verified: Email verification status

        Returns:
            User: Created user instance

        Raises:
            ValueError: If user data is invalid
            Exception: If user already exists
        """
        # Validate email format
        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        # Validate username
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        # Validate password strength
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Check if user already exists
        existing_user = await UserService.get_user_by_email(db, email)
        if existing_user:
            raise Exception("Email already registered")

        existing_username = await UserService.get_user_by_username(db, username)
        if existing_username:
            raise Exception("Username already taken")

        # Create new user
        db_user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_verified=is_verified,
        )
        db_user.set_password(password)

        # Generate verification token if not verified
        if not is_verified:
            db_user.generate_verification_token()

        # Save to database
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        logger.info("User created", user_id=db_user.id, username=username, email=email)
        return db_user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        username_or_email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with username/email and password.

        Args:
            db: Database session
            username_or_email: Username or email address
            password: Plain text password

        Returns:
            User or None if authentication fails
        """
        # Get user by username or email
        user = await UserService.get_user_by_username_or_email(db, username_or_email)
        if not user:
            return None

        # Check if user is active
        if not user.is_active:
            logger.warning("Inactive user login attempt", user_id=user.id, username=user.username)
            return None

        # Verify password
        if not user.verify_password(password):
            logger.warning("Invalid password attempt", user_id=user.id, username=user.username)
            return None

        # Update last login
        user.update_last_login()
        await db.commit()

        logger.info("User authenticated", user_id=user.id, username=user.username)
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User or None if not found
        """
        result = await db.get(User, user_id)
        return result

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            db: Database session
            email: Email address

        Returns:
            User or None if not found
        """
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            db: Database session
            username: Username

        Returns:
            User or None if not found
        """
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username_or_email(
        db: AsyncSession,
        username_or_email: str
    ) -> Optional[User]:
        """
        Get user by username or email.

        Args:
            db: Database session
            username_or_email: Username or email

        Returns:
            User or None if not found
        """
        query = select(User).where(
            and_(
                User.email == username_or_email,
                User.username == username_or_email
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def verify_user_email(db: AsyncSession, verification_token: str) -> bool:
        """
        Verify user email with token.

        Args:
            db: Database session
            verification_token: Email verification token

        Returns:
            bool: True if verification successful
        """
        query = select(User).where(User.verification_token == verification_token)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return False

        user.verify_email()
        await db.commit()

        logger.info("User email verified", user_id=user.id, username=user.username)
        return True

    @staticmethod
    async def reset_password(db: AsyncSession, user: User, new_password: str) -> bool:
        """
        Reset user password.

        Args:
            db: Database session
            user: User instance
            new_password: New plain text password

        Returns:
            bool: True if password reset successful
        """
        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        user.set_password(new_password)
        await db.commit()

        logger.info("User password reset", user_id=user.id, username=user.username)
        return True

    @staticmethod
    async def deactivate_user(db: AsyncSession, user: User) -> bool:
        """
        Deactivate user account.

        Args:
            db: Database session
            user: User instance

        Returns:
            bool: True if deactivation successful
        """
        user.deactivate()
        await db.commit()

        logger.info("User deactivated", user_id=user.id, username=user.username)
        return True

    @staticmethod
    async def activate_user(db: AsyncSession, user: User) -> bool:
        """
        Activate user account.

        Args:
            db: Database session
            user: User instance

        Returns:
            bool: True if activation successful
        """
        user.activate()
        await db.commit()

        logger.info("User activated", user_id=user.id, username=user.username)
        return True

    @staticmethod
    async def get_user_statistics(db: AsyncSession) -> Dict[str, Any]:
        """
        Get user statistics for admin dashboard.

        Args:
            db: Database session

        Returns:
            Dict with user statistics
        """
        # Total users
        total_query = select(func.count(User.id)).where(User.is_deleted == False)
        total_result = await db.execute(total_query)
        total_users = total_result.scalar()

        # Active users
        active_query = select(func.count(User.id)).where(
            and_(User.is_active == True, User.is_deleted == False)
        )
        active_result = await db.execute(active_query)
        active_users = active_result.scalar()

        # Verified users
        verified_query = select(func.count(User.id)).where(
            and_(User.is_verified == True, User.is_deleted == False)
        )
        verified_result = await db.execute(verified_query)
        verified_users = verified_result.scalar()

        # Superusers
        superuser_query = select(func.count(User.id)).where(
            and_(User.is_superuser == True, User.is_deleted == False)
        )
        superuser_result = await db.execute(superuser_query)
        superusers = superuser_result.scalar()

        # Recent registrations (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_query = select(func.count(User.id)).where(
            and_(
                User.created_at >= thirty_days_ago,
                User.is_deleted == False
            )
        )
        recent_result = await db.execute(recent_query)
        recent_registrations = recent_result.scalar()

        return {
            "total_users": total_users,
            "active_users": active_users,
            "verified_users": verified_users,
            "superusers": superusers,
            "recent_registrations": recent_registrations,
            "inactive_users": total_users - active_users,
        }

    @staticmethod
    async def search_users(
        db: AsyncSession,
        query: str,
        limit: int = 50
    ) -> List[User]:
        """
        Search users by username or email.

        Args:
            db: Database session
            query: Search query
            limit: Maximum results

        Returns:
            List of matching users
        """
        search_filter = f"%{query}%"
        search_query = select(User).where(
            and_(
                User.is_deleted == False,
                and_(
                    User.username.ilike(search_filter) |
                    User.email.ilike(search_filter)
                )
            )
        ).limit(limit)

        result = await db.execute(search_query)
        return result.scalars().all()

    @staticmethod
    async def update_user_preferences(
        db: AsyncSession,
        user: User,
        preferred_model: Optional[str] = None,
        qwen_api_key: Optional[str] = None
    ) -> User:
        """
        Update user AI preferences.

        Args:
            db: Database session
            user: User instance
            preferred_model: Preferred AI model
            qwen_api_key: User's Qwen API key

        Returns:
            User: Updated user instance
        """
        if preferred_model:
            user.preferred_model = preferred_model
        if qwen_api_key:
            user.qwen_api_key = qwen_api_key

        user.touch()
        await db.commit()
        await db.refresh(user)

        logger.info(
            "User preferences updated",
            user_id=user.id,
            username=user.username,
            preferred_model=preferred_model
        )

        return user

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a secure random token.

        Args:
            length: Token length in bytes

        Returns:
            str: Secure token
        """
        return secrets.token_urlsafe(length)