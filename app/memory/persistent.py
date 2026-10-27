from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


class ConsentMemoryStore:
    """Simple file-backed memory store with explicit consent checks."""

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.getenv("MEMORY_STORE_PATH", "memory_store.json")
        self._store = self._load_store()

    def _load_store(self) -> Dict[str, Any]:
        if not os.path.exists(self.storage_path):
            return {"sessions": {}}

        try:
            with open(self.storage_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, dict):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
        return {"sessions": {}}

    def _save_store(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as handle:
            json.dump(self._store, handle, indent=2)

    def remember(
        self,
        session_id: str,
        topic: str,
        fact: str,
        consent: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not consent:
            return {"stored": False, "reason": "Memory not stored because consent was not provided."}

        session_entry = self._store.setdefault("sessions", {}).setdefault(session_id, {"memories": []})
        record = {
            "topic": topic,
            "fact": fact,
            "metadata": metadata or {},
        }
        session_entry.setdefault("memories", []).append(record)
        self._save_store()
        return {"stored": True, "memory": record}

    def get_session_memory(self, session_id: str) -> List[Dict[str, Any]]:
        session_entry = self._store.setdefault("sessions", {}).get(session_id, {})
        return session_entry.get("memories", [])

    def clear_session(self, session_id: str) -> None:
        self._store.setdefault("sessions", {}).pop(session_id, None)
        self._save_store()


memory_store = ConsentMemoryStore()


def remember(session_id: str, topic: str, fact: str, consent: bool = False, **metadata: Any) -> Dict[str, Any]:
    return memory_store.remember(session_id, topic, fact, consent=consent, metadata=metadata)
