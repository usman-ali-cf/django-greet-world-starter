from datetime import datetime, timedelta
import secrets
from typing import Dict, Any, Optional
from dateutil.tz import *
import uuid

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=24)  # Session expires after 24 hours of inactivity

    def create_session(self, user_data: Dict[str, Any]) -> str:
        """Create a new session and return the session ID"""
        session_id = str(uuid.uuid4())
        now = datetime.now(tzutc())
        self.sessions[session_id] = {
            'data': user_data,
            'created_at': now.isoformat(),
            'last_activity': now.isoformat()
        }
        return session_id

    def _parse_datetime(self, dt_str: str) -> datetime:
        """Parse ISO format datetime string to datetime object"""
        if isinstance(dt_str, datetime):
            return dt_str
        try:
            # Try parsing with timezone
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            # Fallback to current time if parsing fails
            return datetime.now(tzutc())

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data if it exists and is not expired"""
        if session_id not in self.sessions:
            return None
            
        session_data = self.sessions[session_id]
        now = datetime.now(tzutc())
        
        # Ensure created_at is a datetime object
        created_at = self._parse_datetime(session_data['created_at'])
        
        # Check if session has expired
        if (now - created_at) > self.session_timeout:
            del self.sessions[session_id]
            return None
            
        # Update last activity
        session_data['last_activity'] = now.isoformat()
        return session_data['data']

    def update_session(self, session_id: str, session_data: dict) -> bool:
        """Update an existing session with new data"""
        if session_id in self.sessions:
            # Ensure timestamps are properly formatted
            if 'created_at' not in session_data:
                session_data['created_at'] = self.sessions[session_id].get('created_at', datetime.now(tzutc()).isoformat())
            if 'last_activity' not in session_data:
                session_data['last_activity'] = datetime.now(tzutc()).isoformat()
                
            self.sessions[session_id].update(session_data)
            return True
        return False

    def delete_session(self, session_id: str) -> None:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def clean_expired_sessions(self) -> None:
        """Clean up expired sessions"""
        now = datetime.now()
        expired_sessions = [
            session_id for session_id, session_data in self.sessions.items()
            if (now - session_data['last_activity']) > self.session_timeout
        ]
        for session_id in expired_sessions:
            self.delete_session(session_id)

# Global session manager instance
session_manager = SessionManager()
