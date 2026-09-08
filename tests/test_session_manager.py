import pytest
from app.core.session import SessionManager


class TestSessionManager:
    """Test session management and tracking."""
    
    @pytest.fixture
    def manager(self):
        return SessionManager()
    
    def test_create_session(self, manager):
        """Test creating a new session."""
        session = manager.create_session("test-session-1")
        
        assert "created_at" in session
        assert session["messages"] == []
        assert session["corrections"] == []
        assert session["total_corrections"] == 0
    
    def test_add_message(self, manager):
        """Test adding a message to a session."""
        manager.create_session("test-session-1")
        
        manager.add_message("test-session-1", "Hello?", {
            "response_text": "Hi there",
            "confidence": {"score": 0.8, "level": "confident"}
        })
        
        session = manager.get_session("test-session-1")
        assert len(session["messages"]) == 1
        assert session["messages"][0]["user_input"] == "Hello?"
    
    def test_record_correction(self, manager):
        """Test recording a user correction."""
        manager.create_session("test-session-1")
        manager.add_message("test-session-1", "Question?", {
            "response_text": "Answer",
            "confidence": {"score": 0.5}
        })
        
        result = manager.record_correction("test-session-1", "Actually, the correct answer is...")
        
        assert result["status"] == "correction recorded"
        assert result["total_corrections"] == 1
        
        session = manager.get_session("test-session-1")
        assert len(session["corrections"]) == 1
        assert session["correction_rate"] == 1.0
    
    def test_correction_rate_calculation(self, manager):
        """Test that correction rate is calculated correctly."""
        manager.create_session("test-session-1")
        
        # Add 3 messages
        for i in range(3):
            manager.add_message("test-session-1", f"Q{i}", {
                "response_text": f"A{i}",
                "confidence": {"score": 0.5}
            })
        
        # Record 1 correction
        manager.record_correction("test-session-1", "Correction")
        
        session = manager.get_session("test-session-1")
        assert session["correction_rate"] == pytest.approx(1/3, rel=0.01)
    
    def test_session_summary(self, manager):
        """Test session summary generation."""
        manager.create_session("test-session-1")
        
        manager.add_message("test-session-1", "Q1", {
            "response_text": "A1",
            "confidence": {"score": 0.8}
        })
        manager.add_message("test-session-1", "Q2", {
            "response_text": "A2",
            "confidence": {"score": 0.6}
        })
        manager.record_correction("test-session-1", "Correction")
        
        summary = manager.get_session_summary("test-session-1")
        
        assert summary["total_messages"] == 2
        assert summary["total_corrections"] == 1
        assert summary["correction_rate"] == 0.5
        assert summary["avg_confidence"] == 0.7
