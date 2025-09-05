"""
Exercise repository for Training Plan Agent.

This module contains the Exercise repository with specific
exercise library operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
from app.database.models import Exercise


class ExerciseRepository(BaseRepository[Exercise]):
    """Exercise repository with exercise-specific operations."""
    
    def __init__(self, db: Session):
        """Initialize exercise repository."""
        super().__init__(Exercise, db)
    
    def create_exercise(self, exercise_data: dict) -> Exercise:
        """Create a new exercise."""
        try:
            exercise = Exercise(**exercise_data)
            self.db.add(exercise)
            self.db.commit()
            self.db.refresh(exercise)
            return exercise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to create exercise: {str(e)}")
    
    def get_exercise_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """Get exercise by ID."""
        try:
            return self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercise by ID: {str(e)}")
    
    def get_exercises_by_category(self, category: str) -> List[Exercise]:
        """Get exercises by category."""
        try:
            return self.db.query(Exercise).filter(Exercise.category == category).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercises by category: {str(e)}")
    
    def get_exercises_by_equipment(self, equipment: str) -> List[Exercise]:
        """Get exercises by equipment."""
        try:
            # Using JSON contains operator for PostgreSQL
            return self.db.query(Exercise).filter(
                Exercise.equipment.contains([equipment])
            ).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercises by equipment: {str(e)}")
    
    def get_exercises_by_difficulty(self, difficulty: str) -> List[Exercise]:
        """Get exercises by difficulty level."""
        try:
            return self.db.query(Exercise).filter(Exercise.difficulty == difficulty).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercises by difficulty: {str(e)}")
    
    def get_exercises_by_muscle_group(self, muscle_group: str) -> List[Exercise]:
        """Get exercises by muscle group."""
        try:
            # Using JSON contains operator for PostgreSQL
            return self.db.query(Exercise).filter(
                Exercise.muscle_groups.contains([muscle_group])
            ).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get exercises by muscle group: {str(e)}")
    
    def search_exercises(self, search_term: str) -> List[Exercise]:
        """Search exercises by name or description."""
        try:
            return self.db.query(Exercise).filter(
                Exercise.name.ilike(f"%{search_term}%") |
                Exercise.description.ilike(f"%{search_term}%")
            ).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to search exercises: {str(e)}")
    
    def update_exercise(self, exercise_id: int, exercise_data: dict) -> Optional[Exercise]:
        """Update exercise by ID."""
        try:
            exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
            if exercise:
                for key, value in exercise_data.items():
                    if hasattr(exercise, key):
                        setattr(exercise, key, value)
                self.db.commit()
                self.db.refresh(exercise)
            return exercise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to update exercise: {str(e)}")
    
    def delete_exercise(self, exercise_id: int) -> bool:
        """Delete exercise by ID."""
        try:
            exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
            if exercise:
                self.db.delete(exercise)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Failed to delete exercise: {str(e)}")
    
    def list_exercises(self) -> List[Exercise]:
        """List all exercises."""
        try:
            return self.db.query(Exercise).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to list exercises: {str(e)}")
