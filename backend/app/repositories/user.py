"""
User repository for Training Plan Agent.

This module contains the User repository with specific
user management operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
from app.database.models import User, UserContext


class UserRepository(BaseRepository[User]):
    """User repository with user-specific operations."""
    
    def __init__(self, db: Session):
        """Initialize user repository."""
        super().__init__(User, db)
    
    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        try:
            user = User(**user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to create user: {str(e)}")
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get user by ID: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get user by email: {str(e)}")
    
    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update user by ID."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                for key, value in user_data.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                self.db.commit()
                self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to update user: {str(e)}")
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                self.db.delete(user)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to delete user: {str(e)}")
    
    def list_users(self) -> List[User]:
        """List all users."""
        try:
            return self.db.query(User).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to list users: {str(e)}")
    
    def create_user_context(self, user_id: int, context_data: dict) -> UserContext:
        """Create user context."""
        try:
            context_data["user_id"] = user_id
            context = UserContext(**context_data)
            self.db.add(context)
            self.db.commit()
            self.db.refresh(context)
            return context
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to create user context: {str(e)}")
    
    def get_user_context(self, user_id: int) -> Optional[UserContext]:
        """Get user context by user ID."""
        try:
            return self.db.query(UserContext).filter(UserContext.user_id == user_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get user context: {str(e)}")
