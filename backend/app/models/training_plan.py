"""
Training plan models for Training Plan Agent.

This module contains models for training plans, plan sessions, and plan exercises.
"""

from datetime import datetime, date
from typing import List, Optional
from pydantic import field_validator
from .base import BaseModel, TimestampMixin


class TrainingPlan(BaseModel, TimestampMixin):
    """Training plan model representing a complete training programme."""
    
    id: Optional[int] = None
    user_id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate plan name is not empty."""
        if not v or not v.strip():
            raise ValueError('Plan name cannot be empty')
        return v.strip()


class PlanSession(BaseModel, TimestampMixin):
    """Plan session model representing a session within a training plan."""
    
    id: Optional[int] = None
    plan_id: int
    session_number: int
    name: str
    description: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None
    
    @field_validator('session_number')
    @classmethod
    def validate_session_number(cls, v: int) -> int:
        """Validate session number is positive."""
        if v <= 0:
            raise ValueError('Session number must be positive')
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate session name is not empty."""
        if not v or not v.strip():
            raise ValueError('Session name cannot be empty')
        return v.strip()
    
    @field_validator('estimated_duration_minutes')
    @classmethod
    def validate_duration(cls, v: Optional[int]) -> Optional[int]:
        """Validate duration is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Duration must be positive')
        return v


class PlanExercise(BaseModel, TimestampMixin):
    """Plan exercise model representing an exercise within a plan session."""
    
    id: Optional[int] = None
    session_id: int
    exercise_id: int
    exercise_order: int
    sets: int
    reps: Optional[int] = None
    reps_range: Optional[str] = None  # e.g., "8-12"
    weight_kg: Optional[float] = None
    weight_percentage: Optional[float] = None  # Percentage of 1RM
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    
    @field_validator('exercise_order')
    @classmethod
    def validate_exercise_order(cls, v: int) -> int:
        """Validate exercise order is positive."""
        if v <= 0:
            raise ValueError('Exercise order must be positive')
        return v
    
    @field_validator('sets')
    @classmethod
    def validate_sets(cls, v: int) -> int:
        """Validate sets is positive."""
        if v <= 0:
            raise ValueError('Sets must be positive')
        return v
    
    @field_validator('reps')
    @classmethod
    def validate_reps(cls, v: Optional[int]) -> Optional[int]:
        """Validate reps is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Reps must be positive')
        return v
    
    @field_validator('weight_kg')
    @classmethod
    def validate_weight(cls, v: Optional[float]) -> Optional[float]:
        """Validate weight is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Weight must be positive')
        return v
    
    @field_validator('weight_percentage')
    @classmethod
    def validate_weight_percentage(cls, v: Optional[float]) -> Optional[float]:
        """Validate weight percentage is between 0 and 100 if provided."""
        if v is not None and (v <= 0 or v > 100):
            raise ValueError('Weight percentage must be between 0 and 100')
        return v
    
    @field_validator('rest_seconds')
    @classmethod
    def validate_rest_seconds(cls, v: Optional[int]) -> Optional[int]:
        """Validate rest seconds is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Rest seconds must be positive')
        return v
