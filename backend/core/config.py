"""
Application configuration module
"""
import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = Field(default="Electrical Project Manager API")
    app_description: str = Field(default="Backend API for Electrical Project Manager")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    
    # JWT Security
    secret_key: str = Field(default="dfedfb48-22ec-4a69-b104-1609c9afe1eb-5nj5e93-4b1c-8f0d-2a5c6e7f8b9a")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=1440)  # 24 hours
    
    # CORS
    allowed_origins: List[str] = Field(default=["http://localhost:8080", "http://localhost:5173"])
    
    # Database
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5433/electric")
    
    # Static files
    static_dir: str = Field(default="static")
    templates_dir: str = Field(default="templates")
    uploads_dir: str = Field(default="uploads")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
