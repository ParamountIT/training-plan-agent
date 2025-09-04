# Training Plan Agent - Architecture Discussion

## Project Overview
An LLM-based solution that uses Airtable training records as knowledge/context to suggest, tweak, and generate comprehensive training plans. The system will support voice logging, progress tracking, and adaptive plan generation.

## Core Requirements
1. **Airtable Integration**: Access training sessions, fitness levels, goals, and gym equipment data
2. **Voice Logging**: Record training sessions through voice input
3. **Plan Generation**: Create comprehensive training plans based on history
4. **Adaptive Adjustments**: Tweak plans based on progress and performance
5. **Historical Analysis**: Use training history for intelligent recommendations

## Proposed Architecture

### 1. Data Layer
```
Airtable (Source of Truth)
├── Training Sessions Table
│   ├── Date, Exercise, Sets, Reps, Weight, RPE, Notes
│   ├── Session Type, Duration, Rest Periods
│   └── Performance Metrics, Subjective Feedback
├── User Profile Table
│   ├── Fitness Level, Goals, Preferences
│   ├── Available Equipment, Gym Access
│   ├── Injury History, Limitations
│   └── Training Frequency, Time Constraints
└── Equipment Table
    ├── Equipment Type, Specifications
    ├── Availability Status, Location
    └── Alternative Options
```

### 2. Application Architecture

#### Backend Services
```
FastAPI Application
├── Airtable Integration Service
│   ├── Data Synchronisation
│   ├── Real-time Updates
│   └── Caching Layer (Redis)
├── Voice Processing Service
│   ├── Speech-to-Text (Whisper/OpenAI)
│   ├── Intent Recognition
│   └── Data Extraction & Validation
├── LLM Service
│   ├── Training Plan Generation
│   ├── Session Analysis
│   ├── Progress Evaluation
│   └── Recommendation Engine
└── Plan Management Service
    ├── Plan Storage & Versioning
    ├── Progress Tracking
    └── Adaptive Adjustments
```

#### Frontend Application
```
React/Next.js Web App
├── Dashboard
│   ├── Current Plan Overview
│   ├── Progress Visualisation
│   └── Quick Actions
├── Voice Logging Interface
│   ├── Recording Controls
│   ├── Real-time Transcription
│   └── Session Review & Edit
├── Plan Management
│   ├── Plan Viewing & Editing
│   ├── Historical Plans
│   └── Customisation Options
└── Analytics & Insights
    ├── Progress Charts
    ├── Performance Trends
    └── Goal Tracking
```

### 3. LLM Integration Strategy

#### Context Management
- **Session Context**: Recent training sessions, current plan status
- **Historical Context**: Long-term progress, pattern recognition
- **User Context**: Goals, preferences, equipment, limitations
- **Environmental Context**: Time constraints, gym availability

#### Prompt Engineering
- **Structured Prompts**: Consistent format for plan generation
- **Few-shot Learning**: Examples from successful training patterns
- **Chain-of-Thought**: Step-by-step reasoning for recommendations
- **Validation Layers**: Consistency checks against user goals

### 4. Data Flow

```
1. Voice Input → Speech-to-Text → Intent Recognition → Data Extraction
2. Airtable Sync → Context Building → LLM Processing → Plan Generation
3. User Review → Plan Approval → Airtable Update → Progress Tracking
4. Performance Analysis → Pattern Recognition → Adaptive Adjustments
```

### 5. Key Components

#### Voice Logging System
- **Real-time Transcription**: Live feedback during recording
- **Intent Recognition**: Identify exercise, sets, reps, weight
- **Data Validation**: Ensure accuracy before saving
- **Offline Capability**: Record without internet, sync later

#### Plan Generation Engine
- **Template System**: Base templates for different training styles
- **Progressive Overload**: Automatic weight/volume progression
- **Periodisation**: Long-term planning with deload weeks
- **Equipment Optimisation**: Maximise available equipment usage

#### Adaptive Learning
- **Performance Tracking**: Monitor progress against predictions
- **Pattern Recognition**: Identify what works for the user
- **Feedback Integration**: Learn from user preferences
- **Goal Alignment**: Ensure plans support user objectives

### 6. Technical Stack Recommendations

#### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL + Redis (caching)
- **LLM**: OpenAI GPT-4 or Anthropic Claude
- **Voice**: OpenAI Whisper API
- **Airtable**: Official Python SDK

#### Frontend
- **Framework**: Next.js 14 with TypeScript
- **UI**: Tailwind CSS + shadcn/ui
- **State**: Zustand or Redux Toolkit
- **Charts**: Recharts or Chart.js
- **Voice**: Web Speech API + MediaRecorder

#### Infrastructure
- **Hosting**: Vercel (frontend) + Railway/Render (backend)
- **Database**: Supabase or PlanetScale
- **Storage**: AWS S3 or Cloudinary (voice files)
- **Monitoring**: Sentry + PostHog

### 7. Security & Privacy Considerations

- **Data Encryption**: All voice recordings encrypted at rest
- **API Security**: Rate limiting, authentication, input validation
- **Privacy Controls**: User data retention policies
- **Airtable Security**: Secure API key management

### 8. Development Phases

#### Phase 1: Foundation
- Airtable integration and data models
- Basic voice logging functionality
- Simple plan generation

#### Phase 2: Intelligence
- Advanced LLM integration
- Progress tracking and analytics
- Adaptive plan adjustments

#### Phase 3: Enhancement
- Advanced voice features
- Comprehensive analytics
- Mobile app (if needed)

## Updated Architecture Based on Requirements

### Database Strategy
- **Current**: Airtable as source of truth
- **Future**: Database-agnostic design for easy migration to PostgreSQL/MySQL
- **Data Layer**: Abstracted repository pattern for seamless transition

### Voice Logging Specification
- **Session Data**: Person name, date, exercise records
- **Exercise Records**: Sets, reps, weight/bodyweight, RPE per set
- **Voice Input**: "3 sets of 8 squats at 100kg, RPE 7" → structured data

### Plan Generation Scope
- **Full Workout Plans**: Complete exercise selection and programming
- **User Context Storage**: Equipment access, goals, fitness level, preferences
- **Adaptive Adjustments**: Modify existing plans based on progress

### Technical Stack
- **LLM**: OpenAI GPT-4 or Anthropic Claude (cloud-based)
- **UI**: Mobile-first responsive design
- **Database**: Repository pattern for future migration

## Implementation Plan

### Phase 1: Foundation & Data Integration
1. **Airtable Schema Analysis**: Review your current structure
2. **Database Abstraction Layer**: Create repository pattern for data access
3. **Voice Logging MVP**: Basic speech-to-text for session recording
4. **Data Models**: User profile, training sessions, equipment, goals

### Phase 2: LLM Integration & Plan Generation
1. **Context Management**: Build comprehensive user context from Airtable
2. **Plan Generation Engine**: Full workout plan creation with exercise selection
3. **Voice Data Processing**: Extract structured data from voice input
4. **Mobile-First UI**: Responsive interface for voice logging and plan viewing

### Phase 3: Intelligence & Adaptation
1. **Progress Tracking**: Monitor performance against plans
2. **Adaptive Adjustments**: Modify plans based on progress and feedback
3. **Advanced Analytics**: Long-term progress visualisation
4. **Database Migration**: Optional transition from Airtable to relational DB

## Next Steps

1. **Airtable Access**: Please share your Airtable schema or provide access
2. **Repository Pattern**: Design database-agnostic data layer
3. **Voice Processing**: Implement speech-to-text with structured data extraction
4. **Mobile UI**: Create responsive interface for voice logging and plan management

Would you like to proceed with sharing your Airtable schema so we can start the implementation?
