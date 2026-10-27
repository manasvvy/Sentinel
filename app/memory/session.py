from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.memory.persistent import memory_store


class SessionMemory:
    """Thin wrapper around the consent-aware memory store."""

    def __init__(self, store=None):
        self.store = store or memory_store

    def save(self, session_id: str, topic: str, fact: str, consent: bool = False, **metadata: Any) -> Dict[str, Any]:
        return self.store.remember(session_id, topic, fact, consent=consent, metadata=metadata)

    def get(self, session_id: str) -> List[Dict[str, Any]]:
        return self.store.get_session_memory(session_id)

    def clear(self, session_id: str) -> None:
        self.store.clear_session(session_id)


session_memory = SessionMemory()


def get_session_memory(session_id: str) -> List[Dict[str, Any]]:
    return session_memory.get(session_id)
