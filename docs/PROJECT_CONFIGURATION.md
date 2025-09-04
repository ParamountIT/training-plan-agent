# Project Configuration & Environment Setup

## Overview
Comprehensive configuration setup for the Training Plan Agent project, including environment variables, API keys, security measures, and development standards.

## Environment Configuration

### Environment Files Structure
```
training_plan_agent/
├── .env.example              # Template with all required variables
├── .env.local                 # Local development (gitignored)
├── .env.staging              # Staging environment (gitignored)
├── .env.production           # Production environment (gitignored)
├── backend/
│   ├── .env.example          # Backend-specific template
│   └── .env.local            # Backend local environment
└── frontend/
    ├── .env.example          # Frontend-specific template
    └── .env.local            # Frontend local environment
```

### Backend Environment Variables (.env.example)
```bash
# Application Configuration
APP_NAME=Training Plan Agent
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/training_plan_agent
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Supabase Configuration (Production)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Anthropic Configuration (Alternative)
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Voice Processing Configuration
WHISPER_MODEL=whisper-1
WHISPER_LANGUAGE=en
MAX_AUDIO_DURATION=300  # 5 minutes

# Security Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# File Storage Configuration
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_AUDIO_FORMATS=mp3,wav,m4a
STORAGE_BUCKET=voice-recordings

# Monitoring Configuration
SENTRY_DSN=your-sentry-dsn
LOG_TO_FILE=True
LOG_FILE_PATH=logs/app.log

# Development Configuration
ENABLE_SWAGGER=True
ENABLE_RELOAD=True
```

### Frontend Environment Variables (.env.example)
```bash
# Application Configuration
NEXT_PUBLIC_APP_NAME=Training Plan Agent
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ENVIRONMENT=development

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# OpenAI Configuration (Client-side)
NEXT_PUBLIC_OPENAI_MODEL=gpt-4
NEXT_PUBLIC_OPENAI_MAX_TOKENS=2000

# Voice Processing Configuration
NEXT_PUBLIC_MAX_RECORDING_DURATION=300000  # 5 minutes in ms
NEXT_PUBLIC_ALLOWED_AUDIO_FORMATS=mp3,wav,m4a

# Feature Flags
NEXT_PUBLIC_ENABLE_VOICE_RECORDING=true
NEXT_PUBLIC_ENABLE_REAL_TIME_TRANSCRIPTION=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=false

# Analytics Configuration
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
NEXT_PUBLIC_ENABLE_ANALYTICS=true

# Development Configuration
NEXT_PUBLIC_ENABLE_DEBUG_MODE=true
NEXT_PUBLIC_ENABLE_MOCK_DATA=false
```

## Security Configuration

### API Key Management
```python
# backend/app/utils/security.py
import os
from typing import Optional
from cryptography.fernet import Fernet
import base64

class SecurityManager:
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(self.encryption_key) if self.encryption_key else None
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API keys before storing"""
        if not self.cipher_suite:
            return api_key
        return self.cipher_suite.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API keys when needed"""
        if not self.cipher_suite:
            return encrypted_key
        return self.cipher_suite.decrypt(encrypted_key.encode()).decode()
    
    def validate_api_key(self, api_key: str, service: str) -> bool:
        """Validate API key format and test connection"""
        # Implementation for different services
        pass

# Usage in services
class LLMService:
    def __init__(self):
        self.security_manager = SecurityManager()
        self.openai_key = self.security_manager.decrypt_api_key(
            os.getenv('OPENAI_API_KEY')
        )
```

### Environment Validation
```python
# backend/app/utils/config.py
from pydantic import BaseSettings, validator
from typing import List, Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Training Plan Agent"
    environment: str = "development"
    debug: bool = True
    
    # Database settings
    database_url: str
    
    # API keys
    openai_api_key: str
    anthropic_api_key: Optional[str] = None
    
    # Supabase settings
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    
    # Security settings
    secret_key: str
    algorithm: str = "HS256"
    
    # Validation
    @validator('database_url')
    def validate_database_url(cls, v):
        if not v.startswith('postgresql://'):
            raise ValueError('Invalid database URL format')
        return v
    
    @validator('openai_api_key')
    def validate_openai_key(cls, v):
        if not v.startswith('sk-'):
            raise ValueError('Invalid OpenAI API key format')
        return v
    
    @validator('supabase_url')
    def validate_supabase_url(cls, v):
        if not v.startswith('https://'):
            raise ValueError('Invalid Supabase URL format')
        return v
    
    class Config:
        env_file = ".env.local"
        case_sensitive = False

# Global settings instance
settings = Settings()
```

## Development Environment Setup

### Local Development Stack
```bash
# Required software
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis (optional for caching)
- Git

# Development tools
- VS Code with extensions
- pgAdmin or DBeaver
- Postman or Insomnia
- Docker (optional)
```

### Local Environment Setup Script
```bash
#!/bin/bash
# setup-dev-environment.sh

echo "Setting up Training Plan Agent development environment..."

# Create project directories
mkdir -p backend/app/{models,services,repositories,api,utils}
mkdir -p backend/tests
mkdir -p frontend/src/{app,components,lib,hooks}
mkdir -p frontend/tests
mkdir -p docs
mkdir -p logs

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
pip install pytest pytest-asyncio httpx
pip install openai anthropic supabase
pip install python-multipart python-jose[cryptography] passlib[bcrypt]

# Create requirements.txt
pip freeze > requirements.txt

# Frontend setup
cd ../frontend
npm init -y
npm install next react react-dom typescript @types/node @types/react
npm install @supabase/supabase-js openai
npm install tailwindcss postcss autoprefixer
npm install @testing-library/react @testing-library/jest-dom jest

# Initialize Tailwind CSS
npx tailwindcss init -p

# Create environment files
cd ..
cp .env.example .env.local
cp backend/.env.example backend/.env.local
cp frontend/.env.example frontend/.env.local

echo "Development environment setup complete!"
echo "Please update .env.local files with your API keys and configuration."
```

## Production Configuration

### Deployment Environment Variables
```bash
# Production environment variables (set in hosting platform)
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# Database (Supabase)
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres

# Security
SECRET_KEY=[generated-secret-key]
ENCRYPTION_KEY=[generated-encryption-key]

# API Keys (encrypted)
OPENAI_API_KEY=[encrypted-api-key]
ANTHROPIC_API_KEY=[encrypted-api-key]

# Monitoring
SENTRY_DSN=[sentry-dsn]
```

### Environment-Specific Configurations

#### Development
- Debug mode enabled
- Detailed logging
- Local database
- Mock data available
- Hot reload enabled

#### Staging
- Debug mode disabled
- Info level logging
- Production-like database
- Real API calls
- Performance monitoring

#### Production
- Debug mode disabled
- Warning level logging
- Production database
- Real API calls
- Full monitoring
- Rate limiting
- Security headers

## Configuration Management

### Configuration Classes
```python
# backend/app/utils/config.py
from enum import Enum
from typing import Dict, Any

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class ConfigManager:
    def __init__(self, environment: Environment):
        self.environment = environment
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment"""
        base_config = {
            "app_name": "Training Plan Agent",
            "version": "1.0.0",
            "debug": self.environment == Environment.DEVELOPMENT,
            "log_level": "INFO" if self.environment == Environment.PRODUCTION else "DEBUG",
        }
        
        if self.environment == Environment.DEVELOPMENT:
            base_config.update({
                "database_url": "postgresql://localhost:5432/training_plan_agent",
                "enable_swagger": True,
                "enable_reload": True,
            })
        elif self.environment == Environment.PRODUCTION:
            base_config.update({
                "enable_swagger": False,
                "enable_reload": False,
                "rate_limiting": True,
                "security_headers": True,
            })
        
        return base_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
```

### Environment Validation Script
```python
# scripts/validate_env.py
import os
import sys
from typing import List, Dict

def validate_environment() -> bool:
    """Validate all required environment variables are set"""
    required_vars = {
        'backend': [
            'DATABASE_URL',
            'OPENAI_API_KEY',
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY',
            'SECRET_KEY'
        ],
        'frontend': [
            'NEXT_PUBLIC_API_BASE_URL',
            'NEXT_PUBLIC_SUPABASE_URL',
            'NEXT_PUBLIC_SUPABASE_ANON_KEY'
        ]
    }
    
    missing_vars = []
    
    for section, vars_list in required_vars.items():
        for var in vars_list:
            if not os.getenv(var):
                missing_vars.append(f"{section}: {var}")
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    
    print("✅ All required environment variables are set")
    return True

if __name__ == "__main__":
    success = validate_environment()
    sys.exit(0 if success else 1)
```

## Security Best Practices

### API Key Security
1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Encrypt API keys** before storing in database
4. **Rotate API keys** regularly
5. **Use least privilege** principle for API access

### Database Security
1. **Use connection pooling** to prevent connection exhaustion
2. **Implement proper authentication** and authorization
3. **Use parameterized queries** to prevent SQL injection
4. **Encrypt sensitive data** at rest
5. **Regular backups** with encryption

### Application Security
1. **Input validation** on all endpoints
2. **Rate limiting** to prevent abuse
3. **CORS configuration** for frontend access
4. **Security headers** in production
5. **Error handling** without exposing sensitive information

## Next Steps

1. **Create environment templates** (.env.example files)
2. **Set up local development environment**
3. **Configure security measures**
4. **Validate environment setup**
5. **Begin data migration process**

Would you like to proceed with creating the environment templates and setting up the local development environment?
