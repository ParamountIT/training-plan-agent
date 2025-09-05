"""
Database connection management for Training Plan Agent.

This module handles database connections, session management,
and connection health checks.
"""

from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .base import SessionLocal, engine


class DatabaseConnection:
    """Database connection manager."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection."""
        self.database_url = database_url
        self._connected = False
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected
    
    def connect(self) -> None:
        """Establish database connection."""
        try:
            # Test connection by executing a simple query
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            self._connected = True
        except SQLAlchemyError as e:
            self._connected = False
            raise Exception(f"Failed to connect to database: {str(e)}")
    
    def disconnect(self) -> None:
        """Disconnect from database."""
        self._connected = False
    
    def health_check(self) -> bool:
        """Perform database health check."""
        try:
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            return True
        except SQLAlchemyError:
            return False


def get_database_session() -> Session:
    """Get database session."""
    return SessionLocal()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Database session context manager."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
