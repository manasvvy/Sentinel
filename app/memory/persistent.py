"""
Persistent memory stub for Sentinel.

In the current implementation, all session data lives in memory and
is lost when the server restarts. This module provides the interface
for a future persistent store (database, file-based, or cloud storage).

Design constraints:
- Memory is ALWAYS opt-in (requires explicit user consent)
- No personal or emotional information is stored
- Only factual corrections and topic-level preferences are persisted
- All stored data is auditable and deletable on request

Current state: filesystem-based persistence (JSON files in /tmp or configurable dir).
Production target: swap storage backend without changing the interface.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


# Storage directory — use /tmp for Render (ephemeral is fine for now)
STORAGE_DIR = os.getenv("PERSISTENT_STORAGE_DIR", "/tmp/sentinel_memory")


def _ensure_storage_dir() -> None:
    """Create storage directory if it doesn't exist."""
    os.makedirs(STORAGE_DIR, exist_ok=True)


def _session_path(session_id: str) -> str:
    return os.path.join(STORAGE_DIR, f"{session_id}.json")


def save_corrections(session_id: str, corrections: List[Dict]) -> bool:
    """
    Persist corrections for a session (only if user consented to memory).

    Args:
        session_id: Session identifier
        corrections: List of correction records

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        _ensure_storage_dir()
        data = {
            "session_id": session_id,
            "saved_at": datetime.now().isoformat(),
            "corrections": corrections,
        }
        with open(_session_path(session_id), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except (OSError, IOError):
        return False


def load_corrections(session_id: str) -> Optional[List[Dict]]:
    """
    Load persisted corrections for a session.

    Returns None if no data found (or memory was not consented).
    """
    path = _session_path(session_id)
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("corrections", [])
    except (OSError, json.JSONDecodeError):
        return None


def delete_session_data(session_id: str) -> bool:
    """
    Delete all persisted data for a session.
    Called when user revokes memory consent or requests deletion.

    Returns True if deleted, False if nothing to delete or error.
    """
    path = _session_path(session_id)
    if not os.path.exists(path):
        return False
    try:
        os.remove(path)
        return True
    except OSError:
        return False


def list_persisted_sessions() -> List[str]:
    """Return list of session IDs that have persisted data."""
    try:
        _ensure_storage_dir()
        files = os.listdir(STORAGE_DIR)
        return [f.replace(".json", "") for f in files if f.endswith(".json")]
    except OSError:
        return []
