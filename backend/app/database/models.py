"""
SQLAlchemy database models for Training Plan Agent.

This module contains all SQLAlchemy models that correspond
to the Pydantic models used in the application.
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User database model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Relationships
    user_context = relationship("UserContext", back_populates="user", uselist=False)
    training_sessions = relationship("TrainingSession", back_populates="user")
    training_plans = relationship("TrainingPlan", back_populates="user")


class UserContext(Base, TimestampMixin):
    """User context database model."""
    
    __tablename__ = "user_context"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fitness_level = Column(String(50), nullable=False)
    goals = Column(JSON, nullable=False)
    equipment = Column(JSON, nullable=False)
    preferences = Column(JSON, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_context")


class Exercise(Base, TimestampMixin):
    """Exercise database model."""
    
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    muscle_groups = Column(JSON, nullable=False)
    equipment = Column(JSON, nullable=False)
    difficulty = Column(String(50), nullable=False)
    description = Column(Text)
    instructions = Column(Text)


class TrainingSession(Base, TimestampMixin):
    """Training session database model."""
    
    __tablename__ = "training_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    duration_minutes = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="training_sessions")
    exercise_sets = relationship("ExerciseSet", back_populates="session")


class ExerciseSet(Base, TimestampMixin):
    """Exercise set database model."""
    
    __tablename__ = "exercise_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("training_sessions.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Float)
    rpe = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    session = relationship("TrainingSession", back_populates="exercise_sets")
    exercise = relationship("Exercise")


class TrainingPlan(Base, TimestampMixin):
    """Training plan database model."""
    
    __tablename__ = "training_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="training_plans")
    plan_sessions = relationship("PlanSession", back_populates="plan")


class PlanSession(Base, TimestampMixin):
    """Plan session database model."""
    
    __tablename__ = "plan_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("training_plans.id"), nullable=False)
    session_number = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    estimated_duration_minutes = Column(Integer)
    
    # Relationships
    plan = relationship("TrainingPlan", back_populates="plan_sessions")
    plan_exercises = relationship("PlanExercise", back_populates="session")


class PlanExercise(Base, TimestampMixin):
    """Plan exercise database model."""
    
    __tablename__ = "plan_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("plan_sessions.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    exercise_order = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer)
    reps_range = Column(String(50))
    weight_kg = Column(Float)
    weight_percentage = Column(Float)
    rest_seconds = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    session = relationship("PlanSession", back_populates="plan_exercises")
    exercise = relationship("Exercise")
