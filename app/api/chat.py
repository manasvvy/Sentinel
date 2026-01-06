from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.models.llm_client import call_llm
from app.core.confidence import evaluate_confidence

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # 1. Get raw model output
    model_response = call_llm(request.user_input)

    # 2. Evaluate confidence
    confidence_state = evaluate_confidence(model_response)

    # 3. Return structured response
    return ChatResponse(
        response_text=model_response,
        confidence_state=confidence_state
    )

