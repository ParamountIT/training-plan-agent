"""
Database package for Training Plan Agent.

This package contains all database-related components including
connection management, session handling, and repository patterns.
"""

from .connection import get_database_session, DatabaseConnection
from .base import Base
from .models import User, UserContext, Exercise, TrainingSession, ExerciseSet, TrainingPlan, PlanSession, PlanExercise

__all__ = [
    "get_database_session",
    "DatabaseConnection",
    "Base",
    "User",
    "UserContext", 
    "Exercise",
    "TrainingSession",
    "ExerciseSet",
    "TrainingPlan",
    "PlanSession",
    "PlanExercise"
]
