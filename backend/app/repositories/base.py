"""
Base repository pattern for Training Plan Agent.

This module contains the base repository class with common
CRUD operations that can be inherited by specific repositories.
"""

from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.base import Base

# Generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """Initialize repository with model and database session."""
        self.model = model
        self.db = db
    
    def create(self, data: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        try:
            instance = self.model(**data)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to create record: {str(e)}")
    
    def read(self, id: int) -> Optional[ModelType]:
        """Read a record by ID."""
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to read record: {str(e)}")
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        """Update a record by ID."""
        try:
            instance = self.db.query(self.model).filter(self.model.id == id).first()
            if instance:
                for key, value in data.items():
                    setattr(instance, key, value)
                self.db.commit()
                self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to update record: {str(e)}")
    
    def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        try:
            instance = self.db.query(self.model).filter(self.model.id == id).first()
            if instance:
                self.db.delete(instance)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to delete record: {str(e)}")
    
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """List records with optional filters."""
        try:
            query = self.db.query(self.model)
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            return query.all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to list records: {str(e)}")
