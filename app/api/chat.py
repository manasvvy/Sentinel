from fastapi import APIRouter, HTTPException

from app.core.confidence import evaluate_confidence
from app.core.governance import evaluate_governance
from app.core.logging import audit_logger
from app.core.safety import evaluate_safety
from app.core.session import session_manager
from app.models.llm_client import call_llm
from app.schemas.chat import ChatRequest, ChatResponse, CorrectionRequest, SessionSummaryResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        model_response = call_llm(request.user_input)
        confidence_state = evaluate_confidence(model_response)
        safety_result = evaluate_safety(request.user_input + " " + model_response)
        governance_result = evaluate_governance(
            session_id=request.session_id,
            user_input=request.user_input,
            response_text=model_response,
            confidence_score=confidence_state["score"],
            confidence_level=confidence_state["level"],
            safety_result=safety_result,
        )

        session_manager.add_message(
            request.session_id,
            request.user_input,
            {
                "response_text": model_response,
                "confidence": confidence_state,
                "governance": governance_result,
            },
        )

        audit_logger.log_interaction(
            request.session_id,
            {
                "user_input": request.user_input,
                "response_text": model_response,
                "confidence_score": confidence_state["score"],
                "confidence_level": confidence_state["level"],
                "reasoning": confidence_state["reasoning"],
                "safety": safety_result,
                "governance": governance_result,
            },
        )

        reasons = list(confidence_state["reasoning"])
        if governance_result["status"] in {"review", "caution"}:
            reasons.append(governance_result["reason"])

        return ChatResponse(
            response_text=model_response,
            confidence_state=confidence_state["level"],
            confidence_score=confidence_state["score"],
            reasoning=reasons,
        )
    except Exception as exc:
        audit_logger.log_error(request.session_id, str(exc))
        raise HTTPException(status_code=500, detail=f"Chat error: {str(exc)}") from exc


@router.post("/correct")
def record_correction(request: CorrectionRequest):
    try:
        result = session_manager.record_correction(request.session_id, request.correct_info)
        audit_logger.log_correction(
            request.session_id,
            request.correct_info,
            {"correction_note": request.note} if request.note else {},
        )
        return result
    except Exception as exc:
        audit_logger.log_error(request.session_id, str(exc))
        raise HTTPException(status_code=500, detail=f"Correction error: {str(exc)}") from exc


@router.get("/session/{session_id}/summary", response_model=SessionSummaryResponse)
def get_session_summary(session_id: str):
    summary = session_manager.get_session_summary(session_id)
    if "error" in summary:
        raise HTTPException(status_code=404, detail="Session not found")
    return summary
