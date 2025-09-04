"""
Health check API endpoints.

This module provides health check functionality for monitoring
the application status and ensuring it's running correctly.
"""

from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter
from app.utils.config import get_settings

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns basic information about the application status,
    including version, environment, and timestamp.
    
    Returns:
        Dict[str, Any]: Health check response with status information
    """
    settings = get_settings()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.app_version,
        "environment": settings.environment,
        "app_name": settings.app_name
    }
