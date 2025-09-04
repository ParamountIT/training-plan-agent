"""
Base models for Training Plan Agent.

This module contains base classes and mixins used by all models.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, field_validator, ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        extra="forbid"
    )


class TimestampMixin:
    """Mixin for models with created_at and updated_at timestamps."""
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def set_timestamps(cls, v: Optional[datetime]) -> datetime:
        """Set timestamp to current time if not provided."""
        if v is None:
            return datetime.now()
        return v
