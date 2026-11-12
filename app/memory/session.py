"""
In-memory session store with TTL and cleanup.

Wraps the core SessionManager with additional memory management:
- Session TTL (time-to-live) to avoid unbounded memory growth
- Session metadata for memory consent tracking
- Helper to export session for persistence

This module is the memory abstraction layer — the core SessionManager
handles the data model, this handles lifecycle.
"""

from typing import Dict, Optional, List
from datetime import datetime, timedelta
import uuid


# Default session TTL: 2 hours of inactivity
DEFAULT_TTL_HOURS = 2


class SessionMemoryStore:
    """
    Manages session lifecycle in memory.

    Features:
    - Auto-creates sessions on first access
    - TTL-based expiry (inactive sessions are cleared)
    - Memory consent tracking per session
    - UUID-based session IDs
    """

    def __init__(self, ttl_hours: int = DEFAULT_TTL_HOURS):
        self._sessions: Dict[str, Dict] = {}
        self._last_activity: Dict[str, datetime] = {}
        self._memory_consent: Dict[str, bool] = {}
        self.ttl = timedelta(hours=ttl_hours)

    def create_session(self, memory_consent: bool = False) -> str:
        """Create a new session and return its ID."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "corrections": [],
        }
        self._last_activity[session_id] = datetime.now()
        self._memory_consent[session_id] = memory_consent
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve a session if it exists and hasn't expired."""
        if session_id not in self._sessions:
            return None

        last = self._last_activity.get(session_id)
        if last and (datetime.now() - last) > self.ttl:
            self._expire_session(session_id)
            return None

        self._last_activity[session_id] = datetime.now()
        return self._sessions[session_id]

    def has_memory_consent(self, session_id: str) -> bool:
        """Check if the user has consented to memory for this session."""
        return self._memory_consent.get(session_id, False)

    def set_memory_consent(self, session_id: str, consent: bool) -> None:
        """Update memory consent for a session."""
        self._memory_consent[session_id] = consent

    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None) -> None:
        """Append a message to a session's history."""
        session = self.get_session(session_id)
        if session is None:
            return

        session["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        })

    def get_history(self, session_id: str, last_n: int = 10) -> List[Dict]:
        """Get the last N messages from a session."""
        session = self.get_session(session_id)
        if not session:
            return []
        return session["messages"][-last_n:]

    def list_active_sessions(self) -> List[str]:
        """Return IDs of all active (non-expired) sessions."""
        active = []
        now = datetime.now()
        for sid, last in list(self._last_activity.items()):
            if (now - last) <= self.ttl:
                active.append(sid)
            else:
                self._expire_session(sid)
        return active

    def _expire_session(self, session_id: str) -> None:
        """Remove a session from memory."""
        self._sessions.pop(session_id, None)
        self._last_activity.pop(session_id, None)
        self._memory_consent.pop(session_id, None)

    def cleanup_expired(self) -> int:
        """Remove all expired sessions. Returns count of removed sessions."""
        before = len(self._sessions)
        for sid in list(self._sessions.keys()):
            last = self._last_activity.get(sid)
            if last and (datetime.now() - last) > self.ttl:
                self._expire_session(sid)
        return before - len(self._sessions)


# Global in-memory session store
session_memory = SessionMemoryStore()
