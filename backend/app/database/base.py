"""
SQLAlchemy base configuration for Training Plan Agent.

This module contains the SQLAlchemy base class and common
database configuration.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.utils.config import get_settings

# Create SQLAlchemy base class
Base = declarative_base()


class TimestampMixin:
    """Mixin for SQLAlchemy models with created_at and updated_at timestamps."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Database engine and session factory
def create_database_engine():
    """Create database engine from settings."""
    settings = get_settings()
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.debug
    )


# Create session factory
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
