"""
Configuration management for AURIZA
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    deepgram_api_key: Optional[str] = os.getenv("DEEPGRAM_API_KEY")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./auriza.db")
    mongodb_url: Optional[str] = os.getenv("MONGODB_URL")
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    
    # Voice
    language: str = os.getenv("LANGUAGE", "es")
    voice_sample_rate: int = int(os.getenv("VOICE_SAMPLE_RATE", 16000))
    voice_chunk_size: int = int(os.getenv("VOICE_CHUNK_SIZE", 2048))
    
    # AI
    ai_model: str = os.getenv("AI_MODEL", "gpt-4")
    decision_autonomy_level: str = os.getenv("DECISION_AUTONOMY_LEVEL", "assisted")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Logs
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)"""
    return Settings()
