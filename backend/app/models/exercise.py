"""
Exercise models for Training Plan Agent.

This module contains models for exercises and exercise categories.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import field_validator
from .base import BaseModel, TimestampMixin


class ExerciseCategory(BaseModel):
    """Exercise category model."""
    
    id: Optional[int] = None
    name: str
    description: Optional[str] = None


class Exercise(BaseModel, TimestampMixin):
    """Exercise model representing an exercise in the system."""
    
    id: Optional[int] = None
    name: str
    category: str
    muscle_groups: List[str]
    equipment: List[str]
    difficulty: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Validate exercise category."""
        allowed_categories = ['compound', 'isolation', 'cardio', 'mobility', 'strength']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of: {allowed_categories}')
        return v
    
    @field_validator('muscle_groups')
    @classmethod
    def validate_muscle_groups(cls, v: List[str]) -> List[str]:
        """Validate muscle groups is a list of strings."""
        if not isinstance(v, list):
            raise ValueError('Muscle groups must be a list')
        if not all(isinstance(group, str) for group in v):
            raise ValueError('All muscle groups must be strings')
        return v
    
    @field_validator('equipment')
    @classmethod
    def validate_equipment(cls, v: List[str]) -> List[str]:
        """Validate equipment is a list of strings."""
        if not isinstance(v, list):
            raise ValueError('Equipment must be a list')
        if not all(isinstance(item, str) for item in v):
            raise ValueError('All equipment items must be strings')
        return v
    
    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        """Validate exercise difficulty."""
        allowed_difficulties = ['beginner', 'intermediate', 'advanced']
        if v not in allowed_difficulties:
            raise ValueError(f'Difficulty must be one of: {allowed_difficulties}')
        return v
