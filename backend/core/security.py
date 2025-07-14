"""
Security and authentication utilities
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException, status, Cookie, Depends
from core.config import settings
from session_manager import session_manager


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash"""
    return pwd_context.hash(password)


async def get_current_user_session(
    session_id: str = Cookie(None, alias=settings.session_cookie_name)
) -> dict:
    """
    Get current user session data
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session_data = session_manager.get_session(session_id)
    if not session_data or 'username' not in session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )
    
    return session_data


async def get_current_user(
    session_data: dict = Depends(get_current_user_session)
) -> dict:
    """
    Get current user from session
    """
    return {
        "username": session_data.get("username"),
        "user_id": session_data.get("user_id"),
        "email": session_data.get("email"),
        "full_name": session_data.get("full_name")
    }


def create_session(user_data: dict) -> str:
    """
    Create a new user session
    """
    session_data = {
        'username': user_data.get('username'),
        'user_id': user_data.get('username'),  # Using username as user_id for now
        'email': user_data.get('email'),
        'full_name': user_data.get('full_name'),
        'created_at': datetime.now(timezone.utc).isoformat(),
        'last_activity': datetime.now(timezone.utc).isoformat()
    }
    return session_manager.create_session(session_data)


def delete_session(session_id: str) -> None:
    """
    Delete a user session
    """
    if session_id:
        session_manager.delete_session(session_id)