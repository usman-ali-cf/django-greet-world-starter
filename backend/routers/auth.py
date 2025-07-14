"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from datetime import datetime, timedelta, timezone
from typing import Optional
from schemas.auth import LoginRequest, UserResponse
from services.auth_service import AuthService
from core.security import create_session, delete_session, get_current_user
from core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    redirect_url: Optional[str] = None
):
    """Handle user login and create session"""
    # Get redirect_url from query parameters if not provided
    if not redirect_url:
        query_params = dict(request.query_params)
        redirect_url = query_params.get('redirect_url')
    
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create session
    session_id = create_session(user.dict())
    
    # Set session cookie
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_id,
        max_age=settings.session_lifetime,
        expires=datetime.now(timezone.utc) + timedelta(seconds=settings.session_lifetime),
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite='lax',
        path='/'
    )
    
    return {
        "status": "success",
        "message": "Login successful",
        "user": user.dict(),
        "redirect_url": redirect_url or "/"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(**current_user)


@router.post("/logout")
async def logout(
    response: Response,
    session_id: str = Depends(lambda: None)  # We'll get this from middleware
):
    """Handle user logout"""
    # Session ID will be available from middleware
    if session_id:
        delete_session(session_id)
    
    # Clear session cookie
    response.delete_cookie(settings.session_cookie_name, path='/')
    
    return {
        "status": "success",
        "message": "Logout successful"
    }