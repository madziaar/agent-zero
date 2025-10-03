"""
User management routes for admin operations.

Features:
- List users (admin only)
- Get user by ID (admin only)
- Update user (admin only)
- Delete user (admin only)
- User statistics
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from ..config.database import get_db
from ..middleware.auth import get_current_active_user, require_superuser
from ..models.user import User

router = APIRouter()


# Pydantic models
class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None
    preferred_model: Optional[str] = None


class UserListResponse(BaseModel):
    """Schema for user list response."""
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: str
    last_login: Optional[str]

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """Schema for user statistics."""
    total_users: int
    active_users: int
    verified_users: int
    superusers: int


@router.get("/", response_model=List[UserListResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    search: Optional[str] = Query(None, description="Search by username or email"),
    active_only: bool = Query(True, description="Show only active users"),
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> List[User]:
    """
    List users with pagination and filtering (admin only).

    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        search: Search query for username or email
        active_only: Filter for active users only
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        List of users
    """
    # Build query
    query = select(User)

    # Apply filters
    if active_only:
        query = query.where(User.is_active == True)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            and_(
                User.username.ilike(search_filter) |
                User.email.ilike(search_filter)
            )
        )

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    result = await db.execute(query)
    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserListResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get user by ID (admin only).

    Args:
        user_id: User ID to retrieve
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        User information

    Raises:
        HTTPException: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserListResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Update user information (admin only).

    Args:
        user_id: User ID to update
        user_update: User update data
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        Updated user information

    Raises:
        HTTPException: If user not found
    """
    # Get user from database
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)

    user.touch()
    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Delete user account (admin only).

    Args:
        user_id: User ID to delete
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        Deletion confirmation

    Raises:
        HTTPException: If user not found or trying to delete self
    """
    # Prevent self-deletion
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    # Get user from database
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Soft delete user
    user.soft_delete()
    await db.commit()

    return {"message": "User deleted successfully"}


@router.get("/stats/summary", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get user statistics (admin only).

    Args:
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        User statistics
    """
    # Get total users
    total_result = await db.execute(
        select(func.count(User.id)).where(User.is_deleted == False)
    )
    total_users = total_result.scalar()

    # Get active users
    active_result = await db.execute(
        select(func.count(User.id)).where(
            and_(User.is_active == True, User.is_deleted == False)
        )
    )
    active_users = active_result.scalar()

    # Get verified users
    verified_result = await db.execute(
        select(func.count(User.id)).where(
            and_(User.is_verified == True, User.is_deleted == False)
        )
    )
    verified_users = verified_result.scalar()

    # Get superusers
    superuser_result = await db.execute(
        select(func.count(User.id)).where(
            and_(User.is_superuser == True, User.is_deleted == False)
        )
    )
    superusers = superuser_result.scalar()

    return UserStats(
        total_users=total_users,
        active_users=active_users,
        verified_users=verified_users,
        superusers=superusers
    )


@router.post("/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Activate user account (admin only).

    Args:
        user_id: User ID to activate
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        Activation confirmation

    Raises:
        HTTPException: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.activate()
    await db.commit()

    return {"message": "User activated successfully"}


@router.post("/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Deactivate user account (admin only).

    Args:
        user_id: User ID to deactivate
        current_user: Current authenticated superuser
        db: Database session

    Returns:
        Deactivation confirmation

    Raises:
        HTTPException: If user not found or trying to deactivate self
    """
    # Prevent self-deactivation
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.deactivate()
    await db.commit()

    return {"message": "User deactivated successfully"}