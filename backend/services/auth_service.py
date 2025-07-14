"""
Authentication service
"""
from typing import Optional
from core.security import verify_password, get_password_hash
from schemas.auth import UserResponse


class AuthService:
    """Service for handling authentication logic"""
    
    # Mock user database - Replace with actual database queries
    _fake_users_db = {
        "admin": {
            "username": "admin",
            "full_name": "Administrator",
            "email": "admin@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
            "disabled": False,
        }
    }
    
    async def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        """
        Authenticate a user with username and password
        """
        user_dict = self._fake_users_db.get(username)
        if not user_dict:
            return None
            
        if not verify_password(password, user_dict["hashed_password"]):
            return None
            
        if user_dict.get("disabled"):
            return None
            
        return UserResponse(**user_dict)
    
    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """
        Get user by username
        """
        user_dict = self._fake_users_db.get(username)
        if user_dict and not user_dict.get("disabled"):
            return UserResponse(**user_dict)
        return None