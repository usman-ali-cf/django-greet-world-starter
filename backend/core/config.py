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
    
    # Security
    secret_key: str = "your-secret-key-here"
    session_cookie_name: str = "session_id"
    session_lifetime: int = 86400  # 24 hours in seconds
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:5173"]
    
    # Database
    database_url: str = "sqlite:///./mysqlite3.db"
    
    # Static files
    static_dir: str = "static"
    templates_dir: str = "templates"
    uploads_dir: str = "uploads"
    
    class Config:
        env_file = ".env"


settings = Settings()