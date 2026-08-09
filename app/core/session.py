from typing import Dict, List, Optional
from datetime import datetime
import json


class SessionManager:
    """
    Manages user sessions, message history, and corrections.
    Tracks confidence calibration and learning signals.
    """
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self, session_id: str) -> Dict:
        """Initialize a new session."""
        self.sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "corrections": [],
            "confidence_history": [],
            "total_corrections": 0,
            "correction_rate": 0.0
        }
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, user_input: str, response_data: Dict) -> None:
        """Record user message and system response."""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        self.sessions[session_id]["messages"].append({
            "user_input": user_input,
            "response_text": response_data.get("response_text"),
            "confidence": response_data.get("confidence"),
            "timestamp": datetime.now().isoformat()
        })
        
        # Track confidence history
        self.sessions[session_id]["confidence_history"].append(
            response_data.get("confidence", {}).get("score", 0.5)
        )
    
    def record_correction(self, session_id: str, correct_info: str) -> Dict:
        """
        Record user correction—this is Sentinel's primary learning signal.
        Corrections indicate the model was wrong or unclear.
        """
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        session = self.sessions[session_id]
        session["corrections"].append({
            "corrected_info": correct_info,
            "timestamp": datetime.now().isoformat(),
            "message_count": len(session["messages"])
        })
        
        # Update correction rate
        session["total_corrections"] = len(session["corrections"])
        if len(session["messages"]) > 0:
            session["correction_rate"] = session["total_corrections"] / len(session["messages"])
        
        return {
            "status": "correction recorded",
            "total_corrections": session["total_corrections"]
        }
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session data."""
        return self.sessions.get(session_id)
    
    def get_session_summary(self, session_id: str) -> Dict:
        """Get summary statistics for a session."""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        session = self.sessions[session_id]
        avg_confidence = (
            sum(session["confidence_history"]) / len(session["confidence_history"])
            if session["confidence_history"]
            else 0
        )
        
        return {
            "session_id": session_id,
            "created_at": session["created_at"],
            "total_messages": len(session["messages"]),
            "total_corrections": session["total_corrections"],
            "correction_rate": round(session["correction_rate"], 2),
            "avg_confidence": round(avg_confidence, 2),
            "confidence_trend": session["confidence_history"][-5:] if session["confidence_history"] else []
        }


# Global session manager instance
session_manager = SessionManager()
