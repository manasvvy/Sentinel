from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, CorrectionRequest, SessionSummaryResponse
from app.models.llm_client import call_llm
from app.core.confidence import evaluate_confidence
from app.core.session import session_manager
from app.core.logging import audit_logger
from app.core.safety import evaluate_safety
from app.core.governance import governance_engine
from app.monitoring.metrics import metrics

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint with confidence evaluation.

    Flow:
    1. Get raw model output
    2. Run safety evaluation (input + response)
    3. Evaluate confidence (adjusted by safety penalties)
    4. Track in session + governance
    5. Log for audit
    6. Return structured response
    """
    try:
        # 1. Get raw model output
        model_response = call_llm(request.user_input)

        # 2. Safety evaluation
        safety_report = evaluate_safety(request.user_input, model_response)

        # 3. Evaluate confidence (apply safety penalty if overconfident)
        confidence_state = evaluate_confidence(model_response)
        if safety_report["confidence_penalty"] > 0:
            adjusted_score = max(
                0.0,
                confidence_state["score"] - safety_report["confidence_penalty"]
            )
            confidence_state["score"] = round(adjusted_score, 2)
            confidence_state["reasoning"].append(
                f"Confidence penalised for overconfident language (−{safety_report['confidence_penalty']:.2f})"
            )
            # Recalculate level after penalty
            if adjusted_score >= 0.7:
                confidence_state["level"] = "confident"
            elif adjusted_score >= 0.4:
                confidence_state["level"] = "cautious"
            else:
                confidence_state["level"] = "guessing"

        # 4. Track in session
        session_manager.add_message(request.session_id, request.user_input, {
            "response_text": model_response,
            "confidence": confidence_state
        })

        # 5. Record in governance + metrics
        governance_engine.record_interaction(
            session_id=request.session_id,
            confidence_score=confidence_state["score"],
            confidence_level=confidence_state["level"],
            safety_flags=(
                safety_report["input_safety"]["flags"] +
                safety_report["response_safety"]["flags"]
            ),
        )
        metrics.record_interaction(
            confidence_score=confidence_state["score"],
            confidence_level=confidence_state["level"],
        )
        if safety_report["response_safety"]["flags"]:
            metrics.record_safety_flag()

        # 6. Audit log
        audit_logger.log_interaction(request.session_id, {
            "user_input": request.user_input,
            "response_text": model_response,
            "confidence_score": confidence_state["score"],
            "confidence_level": confidence_state["level"],
            "reasoning": confidence_state["reasoning"],
            "safety_flags": safety_report["input_safety"]["flags"] + safety_report["response_safety"]["flags"],
        })

        # 7. Return structured response
        return ChatResponse(
            response_text=model_response,
            confidence_state=confidence_state["level"],
            confidence_score=confidence_state["score"],
            reasoning=confidence_state["reasoning"]
        )
    except Exception as e:
        metrics.record_error()
        audit_logger.log_error(request.session_id, str(e))
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/correct")
def record_correction(request: CorrectionRequest):
    """
    Record user correction — Sentinel's primary learning signal.
    When a user corrects the system, we learn and adjust confidence.
    """
    try:
        result = session_manager.record_correction(
            request.session_id,
            request.correct_info
        )

        governance_engine.record_correction(request.session_id)
        metrics.record_correction()

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

    Primary signal: correction rate (increase over time = better calibration)
    Supporting signals: confidence calibration, usage patterns
    """
    summary = session_manager.get_session_summary(session_id)
    if "error" in summary:
        raise HTTPException(status_code=404, detail="Session not found")
    return summary


@router.get("/metrics")
def get_metrics():
    """System-wide metrics (operational monitoring)."""
    return metrics.get_summary()


@router.get("/governance")
def get_governance():
    """Global governance report."""
    return governance_engine.get_global_report()
