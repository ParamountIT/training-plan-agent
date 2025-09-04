# Data Migration Plan: Airtable to PostgreSQL

## Overview
Direct migration from Airtable to PostgreSQL, eliminating the need for Airtable integration and simplifying the architecture.

## Migration Strategy

### Phase 1: Data Extraction and Analysis
**Goal**: Extract and analyse all Airtable data

#### Tasks
1. **Export Airtable Data**
   - Export Training Sessions table
   - Export Personal Details table
   - Export Exercises table
   - Export Training Plans table

2. **Data Analysis**
   - Identify data quality issues
   - Map relationships between tables
   - Identify missing or inconsistent data
   - Plan data normalisation

3. **Schema Validation**
   - Validate against proposed PostgreSQL schema
   - Identify required transformations
   - Plan data type conversions
   - Document data mapping

### Phase 2: PostgreSQL Schema Creation
**Goal**: Create optimised PostgreSQL schema

#### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User context table
CREATE TABLE user_context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    age INTEGER,
    gender VARCHAR(20),
    vo2max FLOAT,
    strength_frequency INTEGER DEFAULT 3,
    running_frequency INTEGER DEFAULT 4,
    max_gym_duration INTEGER DEFAULT 50,
    max_running_monthly INTEGER DEFAULT 160,
    goals TEXT[],
    available_equipment TEXT[],
    preferences JSONB,
    capabilities JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercises table
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),
    muscle_groups TEXT[],
    equipment_required VARCHAR(100),
    movement_pattern VARCHAR(100),
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training plans table
CREATE TABLE training_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    plan_type VARCHAR(100),
    duration_weeks INTEGER,
    frequency_per_week INTEGER,
    session_duration_minutes INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Plan sessions table
CREATE TABLE plan_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES training_plans(id) ON DELETE CASCADE,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 1 AND 7),
    session_name VARCHAR(255),
    focus_areas TEXT[],
    duration_minutes INTEGER,
    notes TEXT,
    order_index INTEGER DEFAULT 0,
    is_rest_day BOOLEAN DEFAULT FALSE
);

-- Plan exercises table
CREATE TABLE plan_exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES plan_sessions(id) ON DELETE CASCADE,
    exercise_id UUID REFERENCES exercises(id),
    exercise_name VARCHAR(255),
    sets INTEGER,
    reps VARCHAR(100),
    weight VARCHAR(100),
    rpe INTEGER CHECK (rpe BETWEEN 0 AND 10),
    rest_seconds INTEGER,
    superset_group INTEGER,
    order_index INTEGER DEFAULT 0,
    notes TEXT
);

-- Training sessions table
CREATE TABLE training_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    plan_id UUID REFERENCES training_plans(id),
    session_date DATE NOT NULL,
    session_name VARCHAR(255),
    duration_minutes INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercise sets table (normalised)
CREATE TABLE exercise_sets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES training_sessions(id) ON DELETE CASCADE,
    exercise_id UUID REFERENCES exercises(id),
    exercise_name VARCHAR(255),
    set_number INTEGER,
    reps INTEGER,
    weight_kg DECIMAL(5,2),
    is_bodyweight BOOLEAN DEFAULT FALSE,
    rpe INTEGER CHECK (rpe BETWEEN 0 AND 10),
    rest_seconds INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_training_sessions_user_date ON training_sessions(user_id, session_date);
CREATE INDEX idx_exercise_sets_session ON exercise_sets(session_id);
CREATE INDEX idx_exercises_name ON exercises(name);
CREATE INDEX idx_plan_sessions_plan ON plan_sessions(plan_id);
```

### Phase 3: Data Transformation and Migration
**Goal**: Transform and migrate data to PostgreSQL

#### Migration Scripts
```python
# Migration script structure
import pandas as pd
import psycopg2
from typing import Dict, List
import json

class AirtableToPostgreSQLMigrator:
    def __init__(self, db_connection_string: str):
        self.conn = psycopg2.connect(db_connection_string)
        self.cursor = self.conn.cursor()
    
    def migrate_users(self, airtable_data: List[Dict]):
        """Migrate user data"""
        for user_data in airtable_data:
            # Extract user information
            name = user_data.get('Name', 'Unknown')
            
            # Insert user
            self.cursor.execute("""
                INSERT INTO users (name) 
                VALUES (%s) 
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, (name,))
            
            user_id = self.cursor.fetchone()[0]
            
            # Migrate user context
            self.migrate_user_context(user_id, user_data)
    
    def migrate_user_context(self, user_id: str, user_data: Dict):
        """Migrate user context from Personal Details"""
        notes = user_data.get('Notes', '')
        
        # Parse notes to extract structured data
        context_data = self.parse_personal_details(notes)
        
        # Insert user context
        self.cursor.execute("""
            INSERT INTO user_context (
                user_id, age, gender, vo2max, goals, 
                available_equipment, preferences, capabilities, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            context_data.get('age'),
            context_data.get('gender'),
            context_data.get('vo2max'),
            context_data.get('goals'),
            context_data.get('equipment'),
            json.dumps(context_data.get('preferences')),
            json.dumps(context_data.get('capabilities')),
            notes
        ))
    
    def migrate_exercises(self, airtable_data: List[Dict]):
        """Migrate exercises data"""
        for exercise_data in airtable_data:
            name = exercise_data.get('Name', '')
            
            # Insert exercise with categorisation
            self.cursor.execute("""
                INSERT INTO exercises (
                    name, category, equipment_required, movement_pattern
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (
                name,
                self.categorise_exercise(name),
                self.get_equipment_required(name),
                self.get_movement_pattern(name)
            ))
    
    def migrate_training_sessions(self, airtable_data: List[Dict]):
        """Migrate training sessions and normalise sets"""
        for session_data in airtable_data:
            # Extract session information
            user_name = session_data.get('Name', '')
            session_date = session_data.get('Date')
            exercise_name = session_data.get('Exercise Name', '')
            num_sets = int(session_data.get('# Sets', 0))
            reps_str = session_data.get('A Reps', '')
            weight_str = session_data.get('A Weight', '')
            rpe = int(session_data.get('# RPE', 0))
            
            # Get user ID
            self.cursor.execute("SELECT id FROM users WHERE name = %s", (user_name,))
            user_id = self.cursor.fetchone()[0]
            
            # Create or get session
            session_id = self.get_or_create_session(user_id, session_date)
            
            # Get exercise ID
            self.cursor.execute("SELECT id FROM exercises WHERE name = %s", (exercise_name,))
            exercise_id = self.cursor.fetchone()[0]
            
            # Parse and insert individual sets
            reps_list = [int(r.strip()) for r in reps_str.split(',')]
            weights_list = weight_str.split(',')
            
            for i in range(num_sets):
                reps = reps_list[i] if i < len(reps_list) else 0
                weight = weights_list[i].strip() if i < len(weights_list) else 'bodyweight'
                
                # Parse weight
                weight_kg = None
                is_bodyweight = False
                
                if weight.lower() == 'bodyweight':
                    is_bodyweight = True
                else:
                    # Extract numeric value from "80kg" format
                    weight_kg = float(weight.replace('kg', ''))
                
                # Insert set
                self.cursor.execute("""
                    INSERT INTO exercise_sets (
                        session_id, exercise_id, exercise_name, set_number,
                        reps, weight_kg, is_bodyweight, rpe
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    session_id, exercise_id, exercise_name, i + 1,
                    reps, weight_kg, is_bodyweight, rpe
                ))
    
    def parse_personal_details(self, notes: str) -> Dict:
        """Parse personal details from notes text"""
        # Implementation to extract structured data from notes
        # This would use regex or NLP to parse the detailed notes
        pass
    
    def categorise_exercise(self, exercise_name: str) -> str:
        """Categorise exercise based on name"""
        # Implementation to categorise exercises
        pass
    
    def get_equipment_required(self, exercise_name: str) -> str:
        """Get equipment required for exercise"""
        # Implementation to determine equipment
        pass
    
    def get_movement_pattern(self, exercise_name: str) -> str:
        """Get movement pattern for exercise"""
        # Implementation to determine movement pattern
        pass
    
    def get_or_create_session(self, user_id: str, session_date: str) -> str:
        """Get or create training session"""
        # Implementation to handle session creation
        pass
```

### Phase 4: Data Validation and Testing
**Goal**: Ensure data integrity and accuracy

#### Validation Tasks
1. **Data Integrity Checks**
   - Verify all records migrated
   - Check for data loss
   - Validate relationships
   - Test constraints

2. **Data Quality Checks**
   - Identify and fix inconsistencies
   - Validate data types
   - Check for missing data
   - Verify business rules

3. **Performance Testing**
   - Test query performance
   - Optimise indexes
   - Monitor resource usage
   - Validate backup procedures

## Benefits of Direct PostgreSQL Migration

### Simplified Architecture
- ✅ **Single database**: No data synchronization complexity
- ✅ **Direct queries**: No API rate limits or delays
- ✅ **Better performance**: Native database operations
- ✅ **Full control**: Complete database control

### Cost Reduction
- ✅ **No Airtable costs**: Eliminate Airtable subscription
- ✅ **Simplified hosting**: Single database to manage
- ✅ **Better scalability**: PostgreSQL scales better
- ✅ **Reduced complexity**: Fewer moving parts

### Development Benefits
- ✅ **Faster development**: No API integration needed
- ✅ **Better testing**: Local database for testing
- ✅ **Easier debugging**: Direct database access
- ✅ **Future-proof**: PostgreSQL is industry standard

## Migration Timeline

### Week 1: Data Extraction
- Export all Airtable data
- Analyse data structure and quality
- Create migration scripts

### Week 2: Schema and Migration
- Set up PostgreSQL database
- Create schema and indexes
- Run migration scripts
- Validate data integrity

### Week 3: Testing and Validation
- Test all functionality
- Optimise performance
- Set up monitoring
- Create backup procedures

## Next Steps

1. **Data Export**: Export all Airtable data
2. **Schema Creation**: Set up PostgreSQL schema
3. **Migration Scripts**: Create data transformation scripts
4. **Testing**: Validate migrated data
5. **Go-Live**: Deploy to production

Would you like to start with the data export and schema creation?
