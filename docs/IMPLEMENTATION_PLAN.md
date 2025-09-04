# Training Plan Agent - Implementation Plan

## Project Overview
Mobile-first LLM-powered training plan agent with voice logging, Airtable integration, and database-agnostic architecture for future migration.

## Technical Architecture

### Database Strategy
- **Current**: Airtable as source of truth
- **Future**: Easy migration to PostgreSQL/MySQL
- **Pattern**: Repository pattern with abstracted data access layer

### Core Data Models
```python
# User Profile
UserProfile:
  - id: str
  - name: str
  - fitness_level: str
  - goals: List[str]
  - available_equipment: List[str]
  - preferences: Dict
  - limitations: List[str]
  - training_frequency: int

# Training Session
TrainingSession:
  - id: str
  - user_id: str
  - date: datetime
  - session_type: str
  - duration_minutes: int
  - notes: str

# Exercise Record
ExerciseRecord:
  - id: str
  - session_id: str
  - exercise_name: str
  - sets: List[SetRecord]
  - notes: str

# Set Record
SetRecord:
  - set_number: int
  - reps: int
  - weight: float  # None for bodyweight
  - rpe: int  # Rate of Perceived Exertion 1-10
  - rest_seconds: int
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Set up project structure and Airtable integration

#### Tasks:
1. **Project Setup**
   - Python virtual environment
   - FastAPI backend structure
   - Next.js mobile-first frontend
   - Repository pattern for data access

2. **Airtable Integration**
   - Schema analysis and mapping
   - Data synchronization service
   - Caching layer (Redis)
   - Error handling and retry logic

3. **Basic Data Models**
   - Pydantic models for all entities
   - Database abstraction layer
   - Airtable to model mapping

4. **Voice Logging MVP**
   - Web Speech API integration
   - Basic speech-to-text
   - Simple data extraction

#### Deliverables:
- Working Airtable integration
- Basic voice logging interface
- Data models and repository pattern
- Mobile-responsive UI shell

### Phase 2: LLM Integration (Week 3-4)
**Goal**: Implement intelligent plan generation and voice processing

#### Tasks:
1. **LLM Service Integration**
   - OpenAI/Anthropic API integration
   - Context management system
   - Prompt engineering for plan generation
   - Response parsing and validation

2. **Voice Data Processing**
   - Advanced speech-to-text with Whisper
   - Intent recognition for exercise logging
   - Data extraction and validation
   - Error handling and correction

3. **Plan Generation Engine**
   - Template-based plan generation
   - Exercise selection algorithms
   - Progressive overload calculations
   - Equipment optimization

4. **Mobile UI Enhancement**
   - Voice recording interface
   - Plan viewing and editing
   - Progress tracking dashboard
   - Offline capability

#### Deliverables:
- Working LLM-powered plan generation
- Advanced voice logging with data extraction
- Mobile-optimized plan management interface
- Context-aware recommendations

### Phase 3: Intelligence & Adaptation (Week 5-6)
**Goal**: Add adaptive learning and comprehensive analytics

#### Tasks:
1. **Progress Tracking**
   - Performance metrics calculation
   - Trend analysis
   - Goal progress monitoring
   - Pattern recognition

2. **Adaptive Adjustments**
   - Plan modification based on progress
   - Automatic weight progression
   - Deload week scheduling
   - Injury prevention recommendations

3. **Advanced Analytics**
   - Progress visualizations
   - Performance insights
   - Goal tracking dashboard
   - Historical analysis

4. **Database Migration Preparation**
   - Migration scripts
   - Data validation
   - Performance optimization
   - Backup strategies

#### Deliverables:
- Adaptive plan adjustment system
- Comprehensive analytics dashboard
- Database migration tools
- Production-ready application

## Project Structure

```
training_plan_agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   └── exercise.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── airtable_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── voice_service.py
│   │   │   └── plan_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base_repository.py
│   │   │   ├── airtable_repository.py
│   │   │   └── postgres_repository.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── sessions.py
│   │   │   ├── plans.py
│   │   │   └── voice.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── config.py
│   │       └── helpers.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── voice/
│   │   │   ├── plans/
│   │   │   └── analytics/
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── utils.ts
│   │   │   └── types.ts
│   │   └── hooks/
│   │       ├── useVoiceRecording.ts
│   │       └── usePlans.ts
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.js
├── docs/
│   ├── ARCHITECTURE_DISCUSSION.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── API_DOCUMENTATION.md
└── README.md
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Airtable (current) → PostgreSQL (future)
- **Caching**: Redis
- **LLM**: OpenAI GPT-4 or Anthropic Claude
- **Voice**: OpenAI Whisper API
- **Authentication**: JWT tokens

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **UI**: Tailwind CSS + shadcn/ui
- **State**: Zustand
- **Charts**: Recharts
- **Voice**: Web Speech API + MediaRecorder

### Infrastructure
- **Hosting**: Vercel (frontend) + Railway (backend)
- **Database**: Supabase (future)
- **Storage**: AWS S3 (voice files)
- **Monitoring**: Sentry

## Development Workflow

### 1. Environment Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Configuration
- Copy `.env.example` to `.env`
- Add Airtable API credentials
- Configure LLM API keys
- Set up Redis connection

### 3. Development
- Backend: `uvicorn app.main:app --reload`
- Frontend: `npm run dev`
- Database: Airtable integration active

## Next Steps

1. **Airtable Schema Review**: Share your current Airtable structure
2. **Environment Setup**: Create development environment
3. **Repository Pattern**: Implement database abstraction layer
4. **Voice Integration**: Set up speech-to-text functionality
5. **Mobile UI**: Create responsive interface

Would you like to start with the Airtable schema analysis and project setup?
