"""
Chat routes - Main conversational interface
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import logging

from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.services.memory_service import MemoryService
from app.services.decision_service import DecisionService
from app.core.personality import personality, CONTEXT_SYSTEM_PROMPT
from app.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])

# Service instances
ai_service = AIService()
memory_service = MemoryService()
decision_service = DecisionService()


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest, settings = Depends(get_settings)):
    \"\"\"
    Send a message to AURIZA
    
    Example:
    {
        \"user_id\": \"user_123\",
        \"message\": \"¿Qué hora es?\",
        \"context\": {\"location\": \"home\"}
    }
    \"\"\"
    
    try:
        # Step 1: Analyze and decide
        decision = await decision_service.analyze_and_decide(
            user_input=request.message,
            user_context=request.context or {},
            user_preferences={}
        )
        
        # Step 2: Store in short-term memory
        await memory_service.store_memory(
            user_id=request.user_id,
            content=request.message,
            memory_type=\"short_term\",
            importance=5
        )
        
        # Step 3: Generate response
        ai_response = await ai_service.generate_response(
            user_message=request.message,
            system_prompt=CONTEXT_SYSTEM_PROMPT,
            context=request.context,
            temperature=0.7
        )
        
        # Step 4: Store response in memory
        await memory_service.store_memory(
            user_id=request.user_id,
            content=f\"Assistant: {ai_response}\",
            memory_type=\"short_term\",
            importance=3
        )
        
        return ChatResponse(
            response=ai_response,
            action=decision.get(\"action\"),
            confidence=decision.get(\"confidence\", 0.0),
            executed=not decision.get(\"requires_confirmation\", True)
        )
        
    except Exception as e:
        logger.error(f\"Error in send_message: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(\"/memory/{user_id}\")
async def get_user_memory(user_id: str, limit: int = 10):
    \"\"\"Get user's recent memories\"\"\"
    
    try:
        profile = await memory_service.get_user_profile(user_id)
        short_term = await memory_service.retrieve_memory(
            user_id=user_id,
            memory_type=\"short_term\",
            limit=limit
        )
        
        return {
            \"user_id\": user_id,
            \"profile\": profile,
            \"recent_memories\": short_term
        }
        
    except Exception as e:
        logger.error(f\"Error in get_user_memory: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(\"/clear-history/{user_id}\")
async def clear_history(user_id: str):
    \"\"\"Clear user's conversation history\"\"\"
    
    try:
        ai_service.clear_history()
        removed = await memory_service.clear_old_memories(user_id, \"short_term\", days_old=0)
        
        return {
            \"status\": \"cleared\",
            \"removed_memories\": removed
        }
        
    except Exception as e:
        logger.error(f\"Error in clear_history: {e}\")
        raise HTTPException(status_code=500, detail=str(e))
