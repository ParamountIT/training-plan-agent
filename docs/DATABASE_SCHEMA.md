# Database Schema Design

## Current Airtable Structure Analysis

### Training Sessions Table (Current)
- **Name**: User name (Laszlo)
- **Date**: Session date
- **# Sets**: Number of sets
- **A Reps**: Comma-separated reps per set (e.g., "10, 10, 10")
- **A Weight**: Comma-separated weights per set (e.g., "30kg, 30kg, 30kg")
- **# RPE**: Rate of Perceived Exertion (0-10)
- **Exercise Name**: Name of the exercise

### Issues with Current Structure
- Multiple values stored in single cells (denormalized)
- Difficult to query individual sets
- Complex data extraction for analysis
- Not suitable for relational database migration

## Proposed Normalized Schema

### 1. Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Exercises Table (Reference)
```sql
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100), -- e.g., "Upper Body", "Lower Body", "Core"
    muscle_groups TEXT[], -- Array of muscle groups
    equipment_required VARCHAR(100), -- e.g., "Barbell", "Dumbbell", "Bodyweight"
    movement_pattern VARCHAR(100), -- e.g., "Push", "Pull", "Squat", "Hinge"
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Training Sessions Table
```sql
CREATE TABLE training_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    session_type VARCHAR(100), -- e.g., "Upper Body", "Lower Body", "Full Body"
    duration_minutes INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Exercise Sets Table (Normalized)
```sql
CREATE TABLE exercise_sets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES training_sessions(id) ON DELETE CASCADE,
    exercise_id UUID REFERENCES exercises(id),
    exercise_name VARCHAR(255) NOT NULL, -- Denormalized for performance
    set_number INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight_kg DECIMAL(5,2), -- NULL for bodyweight exercises
    is_bodyweight BOOLEAN DEFAULT FALSE,
    rpe INTEGER CHECK (rpe BETWEEN 0 AND 10),
    rest_seconds INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. User Context Table
```sql
CREATE TABLE user_context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    fitness_level VARCHAR(50), -- e.g., "Beginner", "Intermediate", "Advanced"
    primary_goals TEXT[], -- Array of goals
    available_equipment TEXT[], -- Array of available equipment
    training_frequency INTEGER, -- Days per week
    session_duration_minutes INTEGER,
    preferences JSONB, -- Flexible preferences storage
    limitations TEXT[], -- Array of limitations/injuries
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Data Migration Strategy

### From Current Airtable to Normalized Structure

#### Step 1: Extract and Transform
```python
def transform_airtable_session(airtable_row):
    """Transform Airtable row to normalized structure"""
    session_data = {
        'user_name': airtable_row['Name'],
        'session_date': airtable_row['Date'],
        'exercises': []
    }
    
    # Parse comma-separated values
    reps = airtable_row['A Reps'].split(', ')
    weights = airtable_row['A Weight'].split(', ')
    num_sets = int(airtable_row['# Sets'])
    
    for i in range(num_sets):
        exercise_set = {
            'exercise_name': airtable_row['Exercise Name'],
            'set_number': i + 1,
            'reps': int(reps[i]),
            'weight_kg': parse_weight(weights[i]),
            'is_bodyweight': weights[i].lower() == 'bodyweight',
            'rpe': int(airtable_row['# RPE'])
        }
        session_data['exercises'].append(exercise_set)
    
    return session_data
```

#### Step 2: Normalize Data
- Create one row per set in `exercise_sets` table
- Link to `training_sessions` table
- Reference `exercises` table for exercise details

## Pydantic Models

### Python Data Models
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date, datetime
from decimal import Decimal

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None

class Exercise(BaseModel):
    id: Optional[str] = None
    name: str
    category: Optional[str] = None
    muscle_groups: List[str] = []
    equipment_required: Optional[str] = None
    movement_pattern: Optional[str] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    instructions: Optional[str] = None

class ExerciseSet(BaseModel):
    id: Optional[str] = None
    session_id: Optional[str] = None
    exercise_id: Optional[str] = None
    exercise_name: str
    set_number: int
    reps: int
    weight_kg: Optional[Decimal] = None
    is_bodyweight: bool = False
    rpe: int = Field(..., ge=0, le=10)
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class TrainingSession(BaseModel):
    id: Optional[str] = None
    user_id: str
    session_date: date
    session_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    exercises: List[ExerciseSet] = []
    created_at: Optional[datetime] = None

class UserContext(BaseModel):
    id: Optional[str] = None
    user_id: str
    fitness_level: Optional[str] = None
    primary_goals: List[str] = []
    available_equipment: List[str] = []
    training_frequency: Optional[int] = None
    session_duration_minutes: Optional[int] = None
    preferences: Optional[dict] = None
    limitations: List[str] = []
    created_at: Optional[datetime] = None
```

## Repository Pattern Implementation

### Abstract Repository
```python
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[BaseModel]:
        pass
    
    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[BaseModel]:
        pass
    
    @abstractmethod
    async def create(self, entity: BaseModel) -> BaseModel:
        pass
    
    @abstractmethod
    async def update(self, id: str, entity: BaseModel) -> BaseModel:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
```

### Airtable Repository
```python
class AirtableRepository(BaseRepository):
    def __init__(self, airtable_client, table_name: str):
        self.client = airtable_client
        self.table_name = table_name
    
    async def get_training_sessions(self, user_name: str) -> List[TrainingSession]:
        # Implementation for Airtable integration
        pass
```

### Future Database Repository
```python
class PostgreSQLRepository(BaseRepository):
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def get_training_sessions(self, user_id: str) -> List[TrainingSession]:
        # Implementation for PostgreSQL
        pass
```

## Benefits of Normalized Structure

1. **Query Performance**: Easy to query individual sets, exercises, or sessions
2. **Data Integrity**: Foreign key constraints ensure data consistency
3. **Analytics**: Simple to calculate progress, trends, and statistics
4. **Scalability**: Better performance as data grows
5. **Flexibility**: Easy to add new fields or relationships
6. **Migration Ready**: Direct path to relational database

## Next Steps

1. **Create Migration Script**: Transform current Airtable data to normalized structure
2. **Implement Repository Pattern**: Abstract data access for easy migration
3. **Build Data Models**: Create Pydantic models for type safety
4. **Test Data Transformation**: Ensure data integrity during migration

Would you like me to proceed with creating the migration script and implementing the repository pattern?
