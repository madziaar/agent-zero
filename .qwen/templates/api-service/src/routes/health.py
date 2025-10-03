"""
Health check endpoints for monitoring and load balancer integration.

Features:
- Basic health check
- Detailed health check with database connectivity
- Readiness and liveness probes
- System metrics and status
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import check_database_connection, get_db
from ..config.settings import settings

router = APIRouter()


@router.get("/", summary="Basic Health Check")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.

    Returns:
        Dict with basic health information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/detailed", summary="Detailed Health Check")
async def detailed_health_check(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Detailed health check with database connectivity test.

    Args:
        db: Database session

    Returns:
        Dict with detailed health information

    Raises:
        HTTPException: If health checks fail
    """
    # Check database connection
    db_healthy = await check_database_connection()

    if not db_healthy:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )

    # Additional health checks can be added here
    # - Redis connectivity
    # - External API endpoints
    # - Disk space
    # - Memory usage

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "checks": {
            "database": "healthy",
            # Add more checks here
        }
    }


@router.get("/ready", summary="Readiness Probe")
async def readiness_check() -> Dict[str, Any]:
    """
    Kubernetes readiness probe endpoint.

    This endpoint should return 200 when the service is ready to accept traffic.
    """
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/live", summary="Liveness Probe")
async def liveness_check() -> Dict[str, Any]:
    """
    Kubernetes liveness probe endpoint.

    This endpoint should return 200 when the service is alive and healthy.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/metrics", summary="System Metrics")
async def system_metrics() -> Dict[str, Any]:
    """
    Get basic system metrics and statistics.

    Returns:
        Dict with system metrics
    """
    import psutil
    import os

    try:
        # System information
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_percent = psutil.cpu_percent(interval=1)

        # Process information
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()

        return {
            "system": {
                "cpu_percent": cpu_percent,
                "memory_total": memory.total,
                "memory_available": memory.available,
                "memory_percent": memory.percent,
                "disk_total": disk.total,
                "disk_free": disk.free,
                "disk_percent": disk.percent,
            },
            "process": {
                "memory_rss": process_memory.rss,
                "memory_vms": process_memory.vms,
                "cpu_num": process.cpu_num() if hasattr(process, 'cpu_num') else None,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "error": f"Failed to get metrics: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }