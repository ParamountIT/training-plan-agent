"""
Session models for Training Plan Agent.

This module contains models for training sessions and exercise sets.
"""

from datetime import datetime, date
from typing import Optional
from pydantic import field_validator
from .base import BaseModel, TimestampMixin


class TrainingSession(BaseModel, TimestampMixin):
    """Training session model representing a workout session."""
    
    id: Optional[int] = None
    user_id: int
    date: date
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    
    @field_validator('duration_minutes')
    @classmethod
    def validate_duration(cls, v: Optional[int]) -> Optional[int]:
        """Validate duration is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Duration must be positive')
        return v


class ExerciseSet(BaseModel, TimestampMixin):
    """Exercise set model representing a single set in a training session."""
    
    id: Optional[int] = None
    session_id: int
    exercise_id: int
    set_number: int
    reps: int
    weight_kg: Optional[float] = None
    rpe: Optional[int] = None
    notes: Optional[str] = None
    
    @field_validator('set_number')
    @classmethod
    def validate_set_number(cls, v: int) -> int:
        """Validate set number is positive."""
        if v <= 0:
            raise ValueError('Set number must be positive')
        return v
    
    @field_validator('reps')
    @classmethod
    def validate_reps(cls, v: int) -> int:
        """Validate reps is positive."""
        if v <= 0:
            raise ValueError('Reps must be positive')
        return v
    
    @field_validator('weight_kg')
    @classmethod
    def validate_weight(cls, v: Optional[float]) -> Optional[float]:
        """Validate weight is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Weight must be positive')
        return v
    
    @field_validator('rpe')
    @classmethod
    def validate_rpe(cls, v: Optional[int]) -> Optional[int]:
        """Validate RPE is between 1 and 10 if provided."""
        if v is not None and (v < 1 or v > 10):
            raise ValueError('RPE must be between 1 and 10')
        return v
