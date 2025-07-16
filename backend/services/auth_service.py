"""
Authentication service
"""
from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.security import verify_password, get_password_hash
from schemas.auth import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from sqlalchemy import or_


class AuthService:
    """Service for handling authentication logic with database integration"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        """
        Authenticate a user with username and password
        """
        # Find user by username or email
        stmt = select(User).where(
            or_(
                User.username == username,
                User.email == username
            )
        )
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        
        if not user or not user.is_active:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return UserResponse(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
    
    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """
        Get user by username or email
        """
        stmt = select(User).where(
            or_(
                User.username == username,
                User.email == username
            )
        )
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        
        if not user or not user.is_active:
            return None
            
        return UserResponse(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
        
    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = None
    ) -> UserResponse:
        """
        Create a new user in the database
        """
        # Check if username or email already exists
        stmt = select(User).where(
            or_(
                User.username == username,
                User.email == email
            )
        )
        result = await self.db.execute(stmt)
        existing_user = result.scalars().first()
        
        if existing_user:
            if existing_user.username == username:
                raise ValueError("Username already registered")
            if existing_user.email == email:
                raise ValueError("Email already registered")
        
        # Hash the password
        hashed_password = get_password_hash(password)
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )
        
        try:
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            
            return UserResponse(
                username=new_user.username,
                email=new_user.email,
                full_name=new_user.full_name,
                is_active=new_user.is_active,
                is_superuser=new_user.is_superuser
            )
            
        except IntegrityError as e:
            await self.db.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                if "username" in str(e):
                    raise ValueError("Username already registered")
                elif "email" in str(e):
                    raise ValueError("Email already registered")
            raise