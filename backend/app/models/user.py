"""
User models for Training Plan Agent.

This module contains models for users and their context/preferences.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import field_validator, EmailStr
from .base import BaseModel, TimestampMixin


class User(BaseModel, TimestampMixin):
    """User model representing a user in the system."""
    
    id: Optional[int] = None
    name: str
    email: EmailStr
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is not empty."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class UserContext(BaseModel, TimestampMixin):
    """User context model containing user preferences and settings."""
    
    id: Optional[int] = None
    user_id: int
    fitness_level: str
    goals: List[str]
    equipment: List[str]
    preferences: Dict[str, Any]
    
    @field_validator('fitness_level')
    @classmethod
    def validate_fitness_level(cls, v: str) -> str:
        """Validate fitness level is one of the allowed values."""
        allowed_levels = ['beginner', 'intermediate', 'advanced']
        if v not in allowed_levels:
            raise ValueError(f'Fitness level must be one of: {allowed_levels}')
        return v
    
    @field_validator('goals')
    @classmethod
    def validate_goals(cls, v: List[str]) -> List[str]:
        """Validate goals is a list of strings."""
        if not isinstance(v, list):
            raise ValueError('Goals must be a list')
        if not all(isinstance(goal, str) for goal in v):
            raise ValueError('All goals must be strings')
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
    
    @field_validator('preferences')
    @classmethod
    def validate_preferences(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate preferences is a dictionary."""
        if not isinstance(v, dict):
            raise ValueError('Preferences must be a dictionary')
        return v
