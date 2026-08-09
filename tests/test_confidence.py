import pytest
from app.core.confidence import evaluate_confidence


class TestConfidenceEngine:
    """Test the confidence evaluation logic."""
    
    def test_confident_response(self):
        """Response with no uncertainty markers should be confident."""
        response = "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
        result = evaluate_confidence(response)
        
        assert result["level"] in ["confident", "cautious"]
        assert result["score"] > 0.6
    
    def test_guessing_response(self):
        """Response with uncertainty markers should be lower confidence."""
        response = "I'm not sure, but machine learning might be related to AI."
        result = evaluate_confidence(response)
        
        assert result["level"] in ["cautious", "guessing"]
        assert "Uncertainty marker found" in str(result["reasoning"])
    
    def test_citation_boost(self):
        """Response with citations should have higher confidence."""
        response_with_citations = "ML uses algorithms [Source: AI Textbook]. This is proven."
        response_without = "ML uses algorithms. This is proven."
        
        result_with = evaluate_confidence(response_with_citations)
        result_without = evaluate_confidence(response_without)
        
        # Citation response should have equal or higher score
        assert result_with["score"] >= result_without["score"]
    
    def test_multiple_reasoning_paths(self):
        """Response with multiple reasons should be more confident."""
        response = "Because of reason A, and because of reason B, the answer is X."
        result = evaluate_confidence(response)
        
        assert "Multiple reasoning paths present" in result["reasoning"]
    
    def test_confidence_normalization(self):
        """Confidence score should be between 0 and 1."""
        responses = [
            "Very confident response with no uncertainty.",
            "I'm not sure, maybe, possibly, definitely might be uncertain.",
            "Regular response."
        ]
        
        for response in responses:
            result = evaluate_confidence(response)
            assert 0 <= result["score"] <= 1
