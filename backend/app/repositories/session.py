"""
Training session repository for Training Plan Agent.

This module contains the Training Session repository with specific
session tracking operations.
"""

from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
from app.database.models import TrainingSession, ExerciseSet


class TrainingSessionRepository(BaseRepository[TrainingSession]):
    """Training session repository with session-specific operations."""
    
    def __init__(self, db: Session):
        """Initialize training session repository."""
        super().__init__(TrainingSession, db)
    
    def create_session(self, session_data: dict) -> TrainingSession:
        """Create a new training session."""
        try:
            session = TrainingSession(**session_data)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            return session
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to create session: {str(e)}")
    
    def get_session_by_id(self, session_id: int) -> Optional[TrainingSession]:
        """Get session by ID."""
        try:
            return self.db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get session by ID: {str(e)}")
    
    def get_sessions_by_user(self, user_id: int) -> List[TrainingSession]:
        """Get sessions by user ID."""
        try:
            return self.db.query(TrainingSession).filter(
                TrainingSession.user_id == user_id
            ).order_by(TrainingSession.date.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get sessions by user: {str(e)}")
    
    def get_sessions_by_date_range(self, start_date: date, end_date: date) -> List[TrainingSession]:
        """Get sessions by date range."""
        try:
            return self.db.query(TrainingSession).filter(
                TrainingSession.date >= start_date,
                TrainingSession.date <= end_date
            ).order_by(TrainingSession.date.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get sessions by date range: {str(e)}")
    
    def get_sessions_by_user_and_date_range(self, user_id: int, start_date: date, end_date: date) -> List[TrainingSession]:
        """Get sessions by user ID and date range."""
        try:
            return self.db.query(TrainingSession).filter(
                TrainingSession.user_id == user_id,
                TrainingSession.date >= start_date,
                TrainingSession.date <= end_date
            ).order_by(TrainingSession.date.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get sessions by user and date range: {str(e)}")
    
    def update_session(self, session_id: int, session_data: dict) -> Optional[TrainingSession]:
        """Update session by ID."""
        try:
            session = self.db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
            if session:
                for key, value in session_data.items():
                    if hasattr(session, key):
                        setattr(session, key, value)
                self.db.commit()
                self.db.refresh(session)
            return session
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to update session: {str(e)}")
    
    def delete_session(self, session_id: int) -> bool:
        """Delete session by ID."""
        try:
            session = self.db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
            if session:
                self.db.delete(session)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to delete session: {str(e)}")
    
    def add_exercise_set(self, set_data: dict) -> ExerciseSet:
        """Add an exercise set to a session."""
        try:
            exercise_set = ExerciseSet(**set_data)
            self.db.add(exercise_set)
            self.db.commit()
            self.db.refresh(exercise_set)
            return exercise_set
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to add exercise set: {str(e)}")
    
    def get_exercise_sets_by_session(self, session_id: int) -> List[ExerciseSet]:
        """Get exercise sets by session ID."""
        try:
            return self.db.query(ExerciseSet).filter(
                ExerciseSet.session_id == session_id
            ).order_by(ExerciseSet.set_number).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercise sets by session: {str(e)}")
    
    def get_exercise_set_by_id(self, set_id: int) -> Optional[ExerciseSet]:
        """Get exercise set by ID."""
        try:
            return self.db.query(ExerciseSet).filter(ExerciseSet.id == set_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercise set by ID: {str(e)}")
    
    def update_exercise_set(self, set_id: int, set_data: dict) -> Optional[ExerciseSet]:
        """Update exercise set by ID."""
        try:
            exercise_set = self.db.query(ExerciseSet).filter(ExerciseSet.id == set_id).first()
            if exercise_set:
                for key, value in set_data.items():
                    if hasattr(exercise_set, key):
                        setattr(exercise_set, key, value)
                self.db.commit()
                self.db.refresh(exercise_set)
            return exercise_set
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to update exercise set: {str(e)}")
    
    def delete_exercise_set(self, set_id: int) -> bool:
        """Delete exercise set by ID."""
        try:
            exercise_set = self.db.query(ExerciseSet).filter(ExerciseSet.id == set_id).first()
            if exercise_set:
                self.db.delete(exercise_set)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to delete exercise set: {str(e)}")
    
    def list_sessions(self) -> List[TrainingSession]:
        """List all sessions."""
        try:
            return self.db.query(TrainingSession).order_by(TrainingSession.date.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to list sessions: {str(e)}")
