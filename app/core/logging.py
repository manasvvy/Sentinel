import json
import os
from datetime import datetime
from typing import Dict, Any


class AuditLogger:
    """
    Logs all system interactions for governance, monitoring, and debugging.
    All decisions are auditable and timestamped.
    """
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file or os.getenv("LOG_FILE", "audit.log")
    
    def log_interaction(self, session_id: str, interaction: Dict[str, Any]) -> None:
        """Log an LLM interaction with all metadata."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "event_type": "llm_interaction",
            **interaction
        }
        self._write_log(entry)
    
    def log_correction(self, session_id: str, correction: str, context: Dict = None) -> None:
        """Log user correction—key safety signal."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "event_type": "user_correction",
            "correction": correction,
            "context": context or {}
        }
        self._write_log(entry)
    
    def log_safety_event(self, session_id: str, event_type: str, details: Dict) -> None:
        """Log safety-related events (overconfidence, unsafe patterns, etc)."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "event_type": f"safety_{event_type}",
            "details": details
        }
        self._write_log(entry)
    
    def log_error(self, session_id: str, error: str, traceback_str: str = None) -> None:
        """Log system errors."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "event_type": "error",
            "error": error,
            "traceback": traceback_str
        }
        self._write_log(entry)
    
    def _write_log(self, entry: Dict[str, Any]) -> None:
        """Write entry to log file."""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except IOError as e:
            print(f"Failed to write to log file: {e}")


# Global audit logger instance
audit_logger = AuditLogger()
