"""
Main FastAPI application for the Training Plan Agent.

This module initialises the FastAPI application and includes
all necessary middleware, routers, and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.utils.config import get_settings

# Get application settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="LLM-powered training plan agent with voice logging and PostgreSQL database",
    debug=settings.debug,
    docs_url="/docs" if settings.enable_swagger else None,
    redoc_url="/redoc" if settings.enable_swagger else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, tags=["health"])


@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns basic information about the application.
    
    Returns:
        Dict: Application information
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs" if settings.enable_swagger else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.enable_reload,
        log_level=settings.log_level.lower()
    )
