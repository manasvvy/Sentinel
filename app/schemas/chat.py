from pydantic import BaseModel
from typing import Literal


class ChatRequest(BaseModel):
    user_input: str
    session_id: str


class ChatResponse(BaseModel):
    response_text: str
    confidence_state: Literal["confident", "guessing"]

