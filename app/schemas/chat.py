from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    user_input: str
    session_id: str


class ChatResponse(BaseModel):
    response_text: str
    confidence_state: str  # "confident", "cautious", or "guessing"
    confidence_score: float  # 0.0 - 1.0
    reasoning: List[str]  # Explanation of confidence determination


class CorrectionRequest(BaseModel):
    session_id: str
    correct_info: str
    note: Optional[str] = None


class SessionSummaryResponse(BaseModel):
    session_id: str
    created_at: str
    total_messages: int
    total_corrections: int
    correction_rate: float
    avg_confidence: float
    confidence_trend: List[float]
