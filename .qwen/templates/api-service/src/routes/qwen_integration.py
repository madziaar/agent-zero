"""
Qwen AI integration routes demonstrating AI-powered features.

Features:
- Text generation and chat endpoints
- Session management for AI conversations
- Token usage tracking and cost estimation
- Streaming responses
- Error handling and retry logic
- Rate limiting for AI requests
"""

import asyncio
import json
import time
import uuid
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
import httpx
import structlog

from ..config.database import get_db
from ..config.settings import settings
from ..middleware.auth import get_current_active_user
from ..middleware.rate_limiting import RateLimitExceeded
from ..models.qwen_session import QwenSession
from ..models.user import User
from ..services.qwen_service import QwenService

router = APIRouter()
logger = structlog.get_logger()


# Pydantic models for requests/responses
class ChatMessage(BaseModel):
    """Schema for chat message."""
    role: str = Field(..., regex="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    """Schema for chat completion request."""
    messages: List[ChatMessage]
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False


class ChatResponse(BaseModel):
    """Schema for chat completion response."""
    session_id: str
    message: ChatMessage
    usage: Dict[str, int]
    model: str
    finish_reason: str


class GenerationRequest(BaseModel):
    """Schema for text generation request."""
    prompt: str
    system_message: Optional[str] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class GenerationResponse(BaseModel):
    """Schema for text generation response."""
    session_id: str
    text: str
    usage: Dict[str, int]
    model: str
    finish_reason: str


class SessionListResponse(BaseModel):
    """Schema for session list response."""
    id: int
    session_id: str
    model: str
    total_tokens: Optional[int]
    is_error: bool
    created_at: str

    class Config:
        from_attributes = True


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create a chat completion with Qwen AI.

    Args:
        request: Chat completion request
        background_tasks: Background tasks for cleanup
        current_user: Authenticated user
        db: Database session

    Returns:
        Chat completion response

    Raises:
        HTTPException: If request fails or rate limit exceeded
        RateLimitExceeded: If user exceeds rate limit
    """
    start_time = time.time()

    # Use user's preferred model or default
    model = request.model or current_user.preferred_model or settings.QWEN_MODEL

    # Prepare messages for Qwen API
    messages = [msg.model_dump() for msg in request.messages]

    # Initialize Qwen service
    qwen_service = QwenService()

    try:
        # Create session record
        session = QwenSession(
            session_id=str(uuid.uuid4()),
            user_id=current_user.id,
            model=model,
            prompt=json.dumps(messages),  # Store as JSON for analysis
        )

        # Make request to Qwen API
        response_data = await qwen_service.chat_completion(
            messages=messages,
            model=model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            user_api_key=current_user.qwen_api_key
        )

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Update session with response data
        session.response = response_data["content"]
        session.finish_reason = response_data["finish_reason"]
        session.prompt_tokens = response_data["usage"]["prompt_tokens"]
        session.completion_tokens = response_data["usage"]["completion_tokens"]
        session.total_tokens = response_data["usage"]["total_tokens"]
        session.response_time_ms = response_time_ms
        session.estimated_cost = response_data.get("estimated_cost", 0)

        # Save session to database (background task)
        db.add(session)
        background_tasks.add_task(save_session, db, session)

        # Prepare response
        response = ChatResponse(
            session_id=session.session_id,
            message=ChatMessage(
                role="assistant",
                content=response_data["content"]
            ),
            usage=response_data["usage"],
            model=model,
            finish_reason=response_data["finish_reason"]
        )

        return response.model_dump()

    except httpx.HTTPStatusError as e:
        # Handle API errors
        error_time_ms = int((time.time() - start_time) * 1000)

        # Create error session record
        session = QwenSession(
            session_id=str(uuid.uuid4()),
            user_id=current_user.id,
            model=model,
            prompt=json.dumps(messages),
            is_error=True,
            error_message=f"API Error: {e.response.status_code}",
            error_code=str(e.response.status_code),
            response_time_ms=error_time_ms
        )
        session.mark_as_error(f"HTTP {e.response.status_code}: {e.response.text}")

        db.add(session)
        background_tasks.add_task(save_session, db, session)

        if e.response.status_code == 429:
            raise RateLimitExceeded(50, 60, int(time.time()) + 60)
        elif e.response.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Qwen API error: {e.response.text}"
            )

    except Exception as e:
        # Handle unexpected errors
        error_time_ms = int((time.time() - start_time) * 1000)

        session = QwenSession(
            session_id=str(uuid.uuid4()),
            user_id=current_user.id,
            model=model,
            prompt=json.dumps(messages),
            is_error=True,
            error_message=str(e),
            response_time_ms=error_time_ms
        )
        session.mark_as_error(f"Unexpected error: {str(e)}")

        db.add(session)
        background_tasks.add_task(save_session, db, session)

        logger.error("Qwen chat completion failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/generate", response_model=GenerationResponse)
async def text_generation(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate text using Qwen AI.

    Args:
        request: Text generation request
        background_tasks: Background tasks for cleanup
        current_user: Authenticated user
        db: Database session

    Returns:
        Text generation response
    """
    start_time = time.time()

    # Use user's preferred model or default
    model = request.model or current_user.preferred_model or settings.QWEN_MODEL

    # Prepare messages for Qwen API
    messages = []
    if request.system_message:
        messages.append({"role": "system", "content": request.system_message})
    messages.append({"role": "user", "content": request.prompt})

    qwen_service = QwenService()

    try:
        # Create session record
        session = QwenSession(
            session_id=str(uuid.uuid4()),
            user_id=current_user.id,
            model=model,
            prompt=request.prompt,
            system_message=request.system_message,
        )

        # Make request to Qwen API
        response_data = await qwen_service.chat_completion(
            messages=messages,
            model=model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            user_api_key=current_user.qwen_api_key
        )

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Update session with response data
        session.response = response_data["content"]
        session.finish_reason = response_data["finish_reason"]
        session.prompt_tokens = response_data["usage"]["prompt_tokens"]
        session.completion_tokens = response_data["usage"]["completion_tokens"]
        session.total_tokens = response_data["usage"]["total_tokens"]
        session.response_time_ms = response_time_ms
        session.estimated_cost = response_data.get("estimated_cost", 0)

        # Save session to database (background task)
        db.add(session)
        background_tasks.add_task(save_session, db, session)

        # Prepare response
        response = GenerationResponse(
            session_id=session.session_id,
            text=response_data["content"],
            usage=response_data["usage"],
            model=model,
            finish_reason=response_data["finish_reason"]
        )

        return response.model_dump()

    except Exception as e:
        logger.error("Qwen text generation failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Text generation failed"
        )


@router.get("/sessions", response_model=List[SessionListResponse])
async def list_sessions(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
) -> List[QwenSession]:
    """
    List user's Qwen AI sessions.

    Args:
        limit: Maximum number of sessions to return
        current_user: Authenticated user
        db: Database session

    Returns:
        List of user's sessions
    """
    from sqlalchemy import select, desc

    query = (
        select(QwenSession)
        .where(QwenSession.user_id == current_user.id)
        .where(QwenSession.is_deleted == False)
        .order_by(desc(QwenSession.created_at))
        .limit(limit)
    )

    result = await db.execute(query)
    sessions = result.scalars().all()

    return sessions


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed session information.

    Args:
        session_id: Session ID to retrieve
        current_user: Authenticated user
        db: Database session

    Returns:
        Detailed session information

    Raises:
        HTTPException: If session not found
    """
    from sqlalchemy import select

    query = select(QwenSession).where(
        QwenSession.session_id == session_id,
        QwenSession.user_id == current_user.id
    )

    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    return session.to_dict()


@router.get("/usage/summary")
async def get_usage_summary(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's AI usage summary and statistics.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        Usage statistics and summary
    """
    from sqlalchemy import select, func, desc

    # Get total token usage
    total_query = select(func.sum(QwenSession.total_tokens)).where(
        QwenSession.user_id == current_user.id,
        QwenSession.is_deleted == False,
        QwenSession.is_error == False
    )
    total_result = await db.execute(total_query)
    total_tokens = total_result.scalar() or 0

    # Get total sessions
    sessions_query = select(func.count(QwenSession.id)).where(
        QwenSession.user_id == current_user.id,
        QwenSession.is_deleted == False
    )
    sessions_result = await db.execute(sessions_query)
    total_sessions = sessions_result.scalar()

    # Get error count
    errors_query = select(func.count(QwenSession.id)).where(
        QwenSession.user_id == current_user.id,
        QwenSession.is_error == True
    )
    errors_result = await db.execute(errors_query)
    error_count = errors_result.scalar()

    # Get total cost
    cost_query = select(func.sum(QwenSession.estimated_cost)).where(
        QwenSession.user_id == current_user.id,
        QwenSession.is_deleted == False
    )
    cost_result = await db.execute(cost_query)
    total_cost = float(cost_result.scalar() or 0)

    # Get average response time
    time_query = select(func.avg(QwenSession.response_time_ms)).where(
        QwenSession.user_id == current_user.id,
        QwenSession.response_time_ms.isnot(None)
    )
    time_result = await db.execute(time_query)
    avg_response_time = float(time_result.scalar() or 0)

    # Get most used model
    model_query = (
        select(QwenSession.model, func.count(QwenSession.id))
        .where(QwenSession.user_id == current_user.id)
        .where(QwenSession.is_deleted == False)
        .group_by(QwenSession.model)
        .order_by(desc(func.count(QwenSession.id)))
        .limit(1)
    )
    model_result = await db.execute(model_query)
    most_used_model = model_result.first()

    return {
        "total_tokens": total_tokens,
        "total_sessions": total_sessions,
        "successful_sessions": total_sessions - error_count,
        "error_count": error_count,
        "success_rate": ((total_sessions - error_count) / total_sessions * 100) if total_sessions > 0 else 0,
        "total_cost": round(total_cost, 4),
        "avg_response_time_ms": round(avg_response_time, 2),
        "most_used_model": most_used_model[0] if most_used_model else None,
        "cost_currency": "USD"
    }


async def save_session(db, session: QwenSession):
    """
    Save session to database in background.

    Args:
        db: Database session
        session: Session to save
    """
    try:
        await db.commit()
        await db.refresh(session)
    except Exception as e:
        logger.error("Failed to save session", error=str(e), session_id=session.session_id)
        await db.rollback()