import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.domains.agentes.service import BellaAgent

router = APIRouter()

class ChatRequest(BaseModel):
    revendedora_id: uuid.UUID
    message: str
    history: Optional[List[Dict[str, str]]] = []

@router.post("/chat")
async def chat_with_bella(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """Interage com a Agente Bella."""
    try:
        agent = BellaAgent(revendedora_id=request.revendedora_id, db_session=db)
        response = await agent.chat(request.message, request.history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
