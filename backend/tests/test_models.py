"""
Tests for Pydantic models.

This module contains comprehensive tests for all Pydantic models
used in the Training Plan Agent application.
"""

import pytest
from datetime import datetime, date
from typing import List, Optional
from pydantic import ValidationError

# Import models
from app.models.user import User, UserContext
from app.models.exercise import Exercise, ExerciseCategory
from app.models.training_plan import TrainingPlan, PlanSession, PlanExercise
from app.models.session import TrainingSession, ExerciseSet


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation_with_valid_data(self):
        """Test creating a user with valid data."""
        user_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        user = User(**user_data)
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
    
    def test_user_creation_without_optional_fields(self):
        """Test creating a user without optional fields."""
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com"
        }
        
        user = User(**user_data)
        assert user.name == "Jane Doe"
        assert user.email == "jane@example.com"
        assert user.id is None  # Should be auto-generated
    
    def test_user_validation_email_format(self):
        """Test email format validation."""
        user_data = {
            "name": "Test User",
            "email": "invalid-email"  # Invalid email format
        }
        
        with pytest.raises(ValidationError):
            User(**user_data)
    
    def test_user_validation_name_required(self):
        """Test that name is required."""
        user_data = {
            "email": "test@example.com"
            # Missing name
        }
        
        with pytest.raises(ValidationError):
            User(**user_data)


class TestUserContextModel:
    """Test cases for UserContext model."""
    
    def test_user_context_creation_with_valid_data(self):
        """Test creating user context with valid data."""
        context_data = {
            "user_id": 1,
            "fitness_level": "intermediate",
            "goals": ["strength", "muscle_gain"],
            "equipment": ["barbell", "dumbbells", "bench"],
            "preferences": {
                "workout_duration": 60,
                "sessions_per_week": 4,
                "preferred_exercises": ["squat", "deadlift", "bench_press"]
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        context = UserContext(**context_data)
        assert context.user_id == 1
        assert context.fitness_level == "intermediate"
        assert len(context.goals) == 2
        assert "barbell" in context.equipment
    
    def test_user_context_validation_fitness_level(self):
        """Test fitness level validation."""
        context_data = {
            "user_id": 1,
            "fitness_level": "invalid_level",  # Invalid fitness level
            "goals": ["strength"],
            "equipment": ["barbell"]
        }
        
        with pytest.raises(ValidationError):
            UserContext(**context_data)
    
    def test_user_context_validation_goals_format(self):
        """Test goals format validation."""
        context_data = {
            "user_id": 1,
            "fitness_level": "beginner",
            "goals": "strength",  # Should be a list, not string
            "equipment": ["barbell"]
        }
        
        with pytest.raises(ValidationError):
            UserContext(**context_data)


class TestExerciseModel:
    """Test cases for Exercise model."""
    
    def test_exercise_creation_with_valid_data(self):
        """Test creating an exercise with valid data."""
        exercise_data = {
            "id": 1,
            "name": "Barbell Squat",
            "category": "compound",
            "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
            "equipment": ["barbell", "rack"],
            "difficulty": "intermediate",
            "description": "A compound lower body exercise",
            "instructions": "Stand with feet shoulder-width apart...",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        exercise = Exercise(**exercise_data)
        assert exercise.id == 1
        assert exercise.name == "Barbell Squat"
        assert exercise.category == "compound"
        assert "quadriceps" in exercise.muscle_groups
    
    def test_exercise_validation_category(self):
        """Test exercise category validation."""
        exercise_data = {
            "name": "Test Exercise",
            "category": "invalid_category",  # Invalid category
            "muscle_groups": ["chest"],
            "equipment": ["barbell"],
            "difficulty": "beginner"
        }
        
        with pytest.raises(ValidationError):
            Exercise(**exercise_data)


class TestTrainingSessionModel:
    """Test cases for TrainingSession model."""
    
    def test_training_session_creation_with_valid_data(self):
        """Test creating a training session with valid data."""
        session_data = {
            "id": 1,
            "user_id": 1,
            "date": date.today(),
            "duration_minutes": 75,
            "notes": "Great session, felt strong today",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        session = TrainingSession(**session_data)
        assert session.id == 1
        assert session.user_id == 1
        assert session.date == date.today()
        assert session.duration_minutes == 75
    
    def test_training_session_validation_duration(self):
        """Test duration validation."""
        session_data = {
            "user_id": 1,
            "date": date.today(),
            "duration_minutes": -10  # Invalid negative duration
        }
        
        with pytest.raises(ValidationError):
            TrainingSession(**session_data)


class TestExerciseSetModel:
    """Test cases for ExerciseSet model."""
    
    def test_exercise_set_creation_with_valid_data(self):
        """Test creating an exercise set with valid data."""
        set_data = {
            "id": 1,
            "session_id": 1,
            "exercise_id": 1,
            "set_number": 1,
            "reps": 8,
            "weight_kg": 100.0,
            "rpe": 8,
            "notes": "Felt heavy but good form",
            "created_at": datetime.now()
        }
        
        exercise_set = ExerciseSet(**set_data)
        assert exercise_set.id == 1
        assert exercise_set.session_id == 1
        assert exercise_set.exercise_id == 1
        assert exercise_set.set_number == 1
        assert exercise_set.reps == 8
        assert exercise_set.weight_kg == 100.0
        assert exercise_set.rpe == 8
    
    def test_exercise_set_validation_rpe_range(self):
        """Test RPE validation (should be 1-10)."""
        set_data = {
            "session_id": 1,
            "exercise_id": 1,
            "set_number": 1,
            "reps": 8,
            "weight_kg": 100.0,
            "rpe": 15  # Invalid RPE (should be 1-10)
        }
        
        with pytest.raises(ValidationError):
            ExerciseSet(**set_data)
    
    def test_exercise_set_validation_weight_positive(self):
        """Test weight validation (should be positive)."""
        set_data = {
            "session_id": 1,
            "exercise_id": 1,
            "set_number": 1,
            "reps": 8,
            "weight_kg": -50.0,  # Invalid negative weight
            "rpe": 8
        }
        
        with pytest.raises(ValidationError):
            ExerciseSet(**set_data)
