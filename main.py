from fastapi import FastAPI, Request, Response, Depends, HTTPException, status, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
import uvicorn
import os
import sys
import json
import logging
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Import database and utility functions
from db_config_sqlite import get_db_connection
from scripts.crea_progetto import crea_progetto
from scripts.carica_file_utenze_mock import _process_excel_and_autoflow, utenze_esistenti, verifica_file_caricato
from scripts.assegna_io import assegna_io_automaticamente
from scripts.crea_nodo import crea_nodo_plc_automatico

# Import session manager
from session_manager import session_manager as global_session_manager

# Initialize FastAPI app
app = FastAPI(title="Electrical Project Manager API",
             description="Backend API for Electrical Project Manager",
             version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

# Database dependency
def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

# Session configuration
SESSION_COOKIE_NAME = "session_id"
SESSION_LIFETIME = 86400  # 24 hours in seconds

# List of paths that don't require authentication
PUBLIC_PATHS = {
    "/login",
    "/static/",
    "/favicon.ico",
    "/api/login",
    "/api/health"
}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Middleware to handle session validation and CSRF protection
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # Skip session check for public paths and OPTIONS requests (preflight)
    if (request.url.path in PUBLIC_PATHS or 
        any(request.url.path.startswith(path) for path in PUBLIC_PATHS if path.endswith('/')) or
        request.method == 'OPTIONS'):
        return await call_next(request)
    
    # Get session ID from cookie
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    
    # Check if session exists and is valid
    if session_id:
        try:
            session_data = global_session_manager.get_session(session_id)
            if session_data:
                # Session is valid, update last activity
                request.state.user = session_data.get('username')
                request.state.session = session_data
                response = await call_next(request)
                
                # Update session last activity
                session_data['last_activity'] = datetime.now(timezone.utc).isoformat()
                global_session_manager.update_session(session_id, session_data)
                
                # Ensure session cookie is set with proper attributes
                if request.url.path != "/api/logout":  # Don't set cookie on logout
                    response.set_cookie(
                        key=SESSION_COOKIE_NAME,
                        value=session_id,
                        max_age=SESSION_LIFETIME,
                        expires=datetime.now(timezone.utc) + timedelta(seconds=SESSION_LIFETIME),
                        httponly=True,
                        secure=False,  # Set to True in production with HTTPS
                        samesite='lax',
                        path='/'  # Make cookie available on all paths
                    )
                return response
        except Exception as e:
            logging.error(f"Session validation error: {str(e)}")
    
    # If we get here, the session is invalid or doesn't exist
    if request.url.path.startswith("/api/"):
        # For API requests, return 401 Unauthorized with CORS headers
        response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Session expired or invalid"}
        )
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    else:
        # For web requests, redirect to login with return URL
        response = RedirectResponse(
            url=f"/login?redirect={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

# Import and include routers
from api import router as api_router
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
