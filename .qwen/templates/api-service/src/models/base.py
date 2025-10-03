"""
Base model for all database models.

Provides common functionality including:
- Timestamps (created_at, updated_at)
- Soft delete support
- Common utility methods
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from ..config.database import Base


class BaseModel(Base):
    """
    Base model with common fields and functionality.

    All models should inherit from this class to get:
    - Automatic timestamps
    - Soft delete support
    - Common utility methods
    """
    __abstract__ = True

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Soft delete
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    @hybrid_property
    def is_active(self) -> bool:
        """Check if the record is active (not soft deleted)."""
        return not self.is_deleted

    def soft_delete(self) -> None:
        """Mark the record as soft deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        """Restore a soft deleted record."""
        self.is_deleted = False
        self.deleted_at = None

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """
        Convert model instance to dictionary.

        Returns:
            dict: Dictionary representation of the model
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if not column.name.startswith('_')
        }

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"