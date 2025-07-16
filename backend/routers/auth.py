
"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import timedelta
from typing import Optional
from pydantic import BaseModel
from schemas.auth import LoginRequest, UserResponse, Token
from services.auth_service import AuthService
from core.security import create_access_token, get_current_user, get_password_hash
from core.config import settings
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db=db)

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    login_data: LoginRequest,
    redirect_url: Optional[str] = None,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Handle user login and return JWT token"""
    # Get redirect_url from query parameters if not provided
    if not redirect_url:
        query_params = dict(request.query_params)
        redirect_url = query_params.get('redirect_url')
    
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.username,  # Using username as user_id for now
            "email": user.email,
            "full_name": user.full_name
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.dict(),
        "redirect_url": redirect_url or "/"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(**current_user)

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Create a new user account
    """
    try:
        # Create the user
        user = await auth_service.create_user(
            username=signup_data.username,
            email=signup_data.email,
            password=signup_data.password,
            full_name=signup_data.full_name
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.username,
                "email": user.email,
                "full_name": user.full_name
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.dict()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout():
    """Handle user logout - with JWT, logout is handled client-side"""
    return {
        "status": "success",
        "message": "Logout successful"
    }
