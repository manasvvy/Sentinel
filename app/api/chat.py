from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, CorrectionRequest, SessionSummaryResponse
from app.models.llm_client import call_llm
from app.core.confidence import evaluate_confidence
from app.core.session import session_manager
from app.core.logging import audit_logger

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint with confidence evaluation.
    
    Flow:
    1. Get raw model output
    2. Evaluate confidence (not just fluency)
    3. Track in session
    4. Log for audit and governance
    5. Return structured response
    """
    try:
        # 1. Get raw model output
        model_response = call_llm(request.user_input)
        
        # 2. Evaluate confidence (now returns detailed dict)
        confidence_state = evaluate_confidence(model_response)
        
        # 3. Track in session
        session_manager.add_message(request.session_id, request.user_input, {
            "response_text": model_response,
            "confidence": confidence_state
        })
        
        # 4. Log for audit and governance
        audit_logger.log_interaction(request.session_id, {
            "user_input": request.user_input,
            "response_text": model_response,
            "confidence_score": confidence_state["score"],
            "confidence_level": confidence_state["level"],
            "reasoning": confidence_state["reasoning"]
        })
        
        # 5. Return structured response
        return ChatResponse(
            response_text=model_response,
            confidence_state=confidence_state["level"],
            confidence_score=confidence_state["score"],
            reasoning=confidence_state["reasoning"]
        )
    except Exception as e:
        audit_logger.log_error(request.session_id, str(e))
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/correct")
def record_correction(request: CorrectionRequest):
    """
    Record user correction—Sentinel's primary learning signal.
    When a user corrects the system, we learn and adjust confidence.
    """
    try:
        result = session_manager.record_correction(
            request.session_id,
            request.correct_info
        )
        
        audit_logger.log_correction(
            request.session_id,
            request.correct_info,
            {"correction_note": request.note} if request.note else {}
        )
        
        return result
    except Exception as e:
        audit_logger.log_error(request.session_id, str(e))
        raise HTTPException(status_code=500, detail=f"Correction error: {str(e)}")


@router.get("/session/{session_id}/summary", response_model=SessionSummaryResponse)
def get_session_summary(session_id: str):
    """
    Get session summary with behavior metrics.
    
    Primary signal: correction rate (increase over time = better)
    Supporting signals: confidence calibration, usage patterns
    """
    summary = session_manager.get_session_summary(session_id)
    if "error" in summary:
        raise HTTPException(status_code=404, detail="Session not found")
    return summary
