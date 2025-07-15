"""
Application configuration module
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Electrical Project Manager API"
    app_description: str = "Backend API for Electrical Project Manager"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # JWT Security
    secret_key: str = "dfedfb48-22ec-4a69-b104-1609c9afe1eb-5nj5e93-4b1c-8f0d-2a5c6e7f8b9a"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:5173"]
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/electric"
    
    # Static files
    static_dir: str = "static"
    templates_dir: str = "templates"
    uploads_dir: str = "uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()
