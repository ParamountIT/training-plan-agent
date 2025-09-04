"""
Configuration management for the Training Plan Agent.

This module handles all configuration settings using Pydantic Settings,
providing type-safe configuration management with environment variable support.
"""

from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings.
    
    This class defines all configuration options for the application,
    with automatic environment variable loading and validation.
    """
    
    # Application settings
    app_name: str = "Training Plan Agent"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database settings
    database_url: str = "postgresql://localhost:5432/training_plan_agent"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Supabase settings
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    
    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.7
    
    # Anthropic settings
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-sonnet-20240229"
    
    # Voice processing settings
    whisper_model: str = "whisper-1"
    whisper_language: str = "en"
    max_audio_duration: int = 300  # 5 minutes
    
    # Security settings
    secret_key: str = "your-secret-key-here-generate-a-secure-random-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # File storage
    max_file_size: int = 10485760  # 10MB
    allowed_audio_formats: List[str] = ["mp3", "wav", "m4a"]
    storage_bucket: str = "voice-recordings"
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    log_to_file: bool = True
    log_file_path: str = "logs/app.log"
    
    # Development settings
    enable_swagger: bool = True
    enable_reload: bool = True
    
    # Validation methods
    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith('postgresql://'):
            raise ValueError('Invalid database URL format')
        return v
    
    @field_validator('openai_api_key')
    @classmethod
    def validate_openai_key(cls, v: Optional[str]) -> Optional[str]:
        """Validate OpenAI API key format."""
        if v and not v.startswith('sk-'):
            raise ValueError('Invalid OpenAI API key format')
        return v
    
    @field_validator('supabase_url')
    @classmethod
    def validate_supabase_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate Supabase URL format."""
        if v and not v.startswith('https://'):
            raise ValueError('Invalid Supabase URL format')
        return v
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        if v not in ['development', 'staging', 'production']:
            raise ValueError('Environment must be development, staging, or production')
        return v
    
    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: The application settings instance
    """
    return settings
