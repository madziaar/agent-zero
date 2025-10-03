"""
Routes package for Qwen API Service Template.
"""

from .auth import router as auth_router
from .health import router as health_router
from .qwen_integration import router as qwen_router
from .users import router as users_router

__all__ = ["auth_router", "health_router", "qwen_router", "users_router"]