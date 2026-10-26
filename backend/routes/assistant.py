"""
FastAPI Multi-Turn NirmanAI Engineering Assistant Route.
"""

from fastapi import APIRouter
from backend.schemas import ChatRequest, ChatResponse
from modules.gemini_client import ConstructionAIClient

router = APIRouter(prefix="/api/assistant", tags=["NirmanAI Assistant Chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_nirman(req: ChatRequest):
    """
    Multi-turn civil engineering and safety chatbot consultation.
    """
    ai_client = ConstructionAIClient(api_key=req.api_key)
    msgs = [{"role": m.role, "content": m.content} for m in req.messages]
    reply, is_live, engine_note = ai_client.chat_response(msgs)

    return ChatResponse(response=reply, is_live=is_live, engine_note=engine_note)
