"""Health check and system status routes."""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, status

from app.core.config import settings

router = APIRouter(tags=["Health & Diagnostics"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
    response_description="Returns basic liveness and health status",
)
async def health_check() -> dict[str, Any]:
    """Liveness probe verifying the FastAPI server is running and responding."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.1.0",
    }


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Subsystem Diagnostic Status",
    response_description="Returns readiness details and subsystem configuration state",
)
async def system_status() -> dict[str, Any]:
    """Readiness probe checking environment configuration and subsystem settings."""
    return {
        "status": "operational",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        "subsystems": {
            "api": "healthy",
            "vector_store_configured": bool(settings.VECTOR_DB_TYPE),
            "vector_store_type": settings.VECTOR_DB_TYPE,
            "llm_model": settings.DEFAULT_LLM_MODEL,
            "embedding_model": settings.DEFAULT_EMBEDDING_MODEL,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
