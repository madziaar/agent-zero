"""
Qwen AI session model for tracking AI interactions.

Features:
- Session management for Qwen AI conversations
- Token usage tracking
- Response time monitoring
- Error tracking and analysis
- Cost calculation
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class QwenSession(BaseModel):
    """
    Model for tracking Qwen AI API interactions and sessions.
    """
    __tablename__ = "qwen_sessions"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # Session identification
    session_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        index=True,
        nullable=True
    )  # Nullable for anonymous sessions

    # Request details
    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )
    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    system_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    # Response details
    response: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    finish_reason: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    # Token usage and performance
    prompt_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    completion_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    total_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    # Performance metrics
    response_time_ms: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Cost tracking (if applicable)
    estimated_cost: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    cost_currency: Mapped[str] = mapped_column(
        String(3),
        default="USD",
        nullable=False
    )

    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    error_code: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    is_error: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )

    # Request parameters
    temperature: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    max_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    top_p: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    # Metadata
    metadata: Mapped[Optional[str]] = mapped_column(
        Text,  # JSON string
        nullable=True
    )

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate session duration in seconds."""
        if self.response_time_ms:
            return self.response_time_ms / 1000.0
        return None

    @property
    def tokens_per_second(self) -> Optional[float]:
        """Calculate token generation speed."""
        if self.total_tokens and self.response_time_ms:
            return (self.total_tokens / self.response_time_ms) * 1000
        return None

    def mark_as_error(self, error_message: str, error_code: Optional[str] = None) -> None:
        """
        Mark the session as having an error.

        Args:
            error_message: Description of the error
            error_code: Error code if available
        """
        self.is_error = True
        self.error_message = error_message
        self.error_code = error_code

    def calculate_cost(self, rate_per_token: float = 0.0001) -> float:
        """
        Calculate estimated cost based on token usage.

        Args:
            rate_per_token: Cost per token in the specified currency

        Returns:
            float: Estimated cost
        """
        if self.total_tokens:
            cost = self.total_tokens * rate_per_token
            self.estimated_cost = cost
            return cost
        return 0.0

    def to_dict(self) -> dict:
        """
        Convert session to dictionary for API responses.

        Returns:
            dict: Session data as dictionary
        """
        data = super().to_dict()
        # Add computed properties
        data.update({
            "duration_seconds": self.duration_seconds,
            "tokens_per_second": self.tokens_per_second,
        })
        return data

    def __repr__(self) -> str:
        """String representation of the session."""
        status = "ERROR" if self.is_error else "SUCCESS"
        return (
            "<QwenSession("
            f"id={self.id}, "
            f"session_id='{self.session_id}', "
            f"model='{self.model}', "
            f"tokens={self.total_tokens}, "
            f"status={status}"
            ")>"
        )