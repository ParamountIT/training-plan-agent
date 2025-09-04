# Training Plan Agent

An LLM-powered training plan agent with voice logging, PostgreSQL database, and mobile-first interface.

## Overview

Training Plan Agent is a comprehensive solution for creating, managing, and adapting personalised training plans using voice input and AI-powered recommendations.

### Key Features

- **Voice Logging**: Record training sessions through voice input
- **LLM-Powered Plans**: Generate and adapt training plans using AI
- **Progress Tracking**: Monitor performance and progress over time
- **Mobile-First**: Responsive design optimised for mobile devices
- **PostgreSQL**: Robust database for data management
- **Real-time Processing**: Live voice transcription and data extraction

## Architecture

### Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (TypeScript)
- **Database**: PostgreSQL (Supabase)
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Voice Processing**: OpenAI Whisper
- **Hosting**: Netlify (Frontend) + Supabase (Backend/Database)

### Project Structure

```
training_plan_agent/
├── docs/                    # Documentation
├── backend/                 # FastAPI backend
├── frontend/                # Next.js frontend
├── .cursorrules             # Development rules
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development Process

### Pre-Development Requirements

1. **GitHub Issues**: All development must be tracked via GitHub issues
2. **TDD Approach**: Test-Driven Development for all features
3. **Code Review**: All code must be reviewed before merging
4. **Documentation**: Comprehensive documentation for all features

### Development Workflow

1. **Create Issue**: Create GitHub issue for feature/bug
2. **Write Tests**: Write failing tests first (TDD)
3. **Implement Feature**: Write code to make tests pass
4. **Code Review**: Submit pull request for review
5. **Merge**: Merge after approval and CI checks pass

### Quality Standards

- **British English**: All comments and documentation
- **Type Hints**: Python type hints everywhere
- **TypeScript Strict**: Frontend strict mode
- **80% Coverage**: Minimum test coverage
- **PEP 8**: Python code style
- **ESLint**: Frontend code quality

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### Local Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd training_plan_agent
   ```

2. **Set Up Environment**
   ```bash
   # Create environment files
   cp docs/env.example .env.local
   cp docs/backend.env.example backend/.env.local
   cp docs/frontend.env.example frontend/.env.local
   
   # Update with your API keys and configuration
   ```

3. **Install Dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

4. **Set Up Database**
   ```bash
   # Create PostgreSQL database
   createdb training_plan_agent
   
   # Run migrations
   cd backend
   python -m alembic upgrade head
   ```

5. **Start Development Servers**
   ```bash
   # Backend (Terminal 1)
   cd backend
   uvicorn app.main:app --reload
   
   # Frontend (Terminal 2)
   cd frontend
   npm run dev
   ```

### Environment Variables

Required environment variables are documented in `docs/PROJECT_CONFIGURATION.md`.

Key variables:
- `OPENAI_API_KEY`: OpenAI API key for LLM and voice processing
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `DATABASE_URL`: PostgreSQL connection string

## Testing

### Backend Testing
```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

### E2E Testing
```bash
npm run test:e2e
```

## Deployment

### Production Deployment

1. **Frontend**: Deploy to Netlify
2. **Backend**: Deploy to Supabase Edge Functions
3. **Database**: Use Supabase PostgreSQL
4. **Environment**: Set production environment variables

### Staging Deployment

1. **Frontend**: Deploy to Netlify (staging branch)
2. **Backend**: Deploy to Supabase Edge Functions (staging)
3. **Database**: Use Supabase PostgreSQL (staging)

## Contributing

### Development Standards

1. **Follow TDD**: Write tests first
2. **Use British English**: All documentation and comments
3. **Follow Style Guides**: PEP 8 for Python, ESLint for TypeScript
4. **Document Changes**: Update documentation for all changes
5. **Code Review**: All changes require review

### Issue Templates

Use appropriate issue templates:
- **Feature Request**: For new features
- **Bug Report**: For bug fixes
- **Documentation**: For documentation updates
- **Enhancement**: For improvements

### Pull Request Process

1. **Create Branch**: From main branch
2. **Write Tests**: Include tests for all changes
3. **Update Documentation**: Update relevant docs
4. **Submit PR**: With clear description and linked issues
5. **Code Review**: Address all review comments
6. **Merge**: After approval and CI checks

## Documentation

- **Architecture**: `docs/ARCHITECTURE_DISCUSSION.md`
- **Implementation Plan**: `docs/IMPLEMENTATION_PLAN.md`
- **Database Schema**: `docs/DATABASE_SCHEMA.md`
- **Deployment Strategy**: `docs/DEPLOYMENT_STRATEGY.md`
- **Project Configuration**: `docs/PROJECT_CONFIGURATION.md`

## License

[License information to be added]

## Support

For support and questions:
- Create GitHub issue
- Check documentation
- Review existing issues

---

**Remember**: No coding without GitHub issues, TDD approach, and proper documentation!
