"""
Decision routes - Autonomous decision-making endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
import logging

from app.models.schemas import Decision
from app.services.decision_service import DecisionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix=\"/api/decisions\", tags=[\"decisions\"])

# Decision service instance
decision_service = DecisionService(autonomy_level=\"assisted\")


@router.post(\"/analyze\")
async def analyze_intent(
    user_id: str,
    user_input: str,
    context: Optional[Dict[str, Any]] = None
) -> dict:
    \"\"\"
    Analyze user input and determine best action
    
    Returns:
    - intent: Detected intent type
    - confidence: Confidence score (0-1)
    - action: Suggested action
    - requires_confirmation: Whether user confirmation is needed
    \"\"\"
    
    try:
        result = await decision_service.analyze_and_decide(
            user_input=user_input,
            user_context=context or {},
            user_preferences={}
        )
        
        return {
            \"user_id\": user_id,
            **result
        }
        
    except Exception as e:
        logger.error(f\"Error in analyze_intent: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(\"/learn\")
async def learn_decision(
    user_id: str,
    intent: str,
    was_correct: bool,
    feedback: Optional[str] = None
) -> dict:
    \"\"\"
    Provide feedback on a decision (for learning)
    \"\"\"
    
    try:
        await decision_service.learn_from_decision(
            intent=intent,
            was_correct=was_correct,
            feedback=feedback
        )
        
        return {
            \"status\": \"learned\",
            \"user_id\": user_id,
            \"intent\": intent,
            \"feedback_recorded\": feedback is not None
        }
        
    except Exception as e:
        logger.error(f\"Error in learn_decision: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(\"/set-autonomy\")
async def set_autonomy_level(user_id: str, level: str) -> dict:
    \"\"\"
    Set autonomy level for a user
    
    Levels:
    - manual: Only responds
    - assisted: Suggests and asks
    - autonomous: Executes and reports
    \"\"\"
    
    if level not in [\"manual\", \"assisted\", \"autonomous\"]:
        raise HTTPException(status_code=400, detail=\"Invalid autonomy level\")
    
    try:
        decision_service.autonomy_level = level
        
        return {
            \"status\": \"updated\",
            \"user_id\": user_id,
            \"autonomy_level\": level
        }
        
    except Exception as e:
        logger.error(f\"Error in set_autonomy_level: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(\"/stats\")
async def get_decision_stats(user_id: Optional[str] = None) -> dict:
    \"\"\"Get decision-making statistics\"\"\"
    
    try:
        return {
            \"autonomy_level\": decision_service.autonomy_level,
            \"patterns_learned\": len(decision_service.learned_patterns),
            \"pattern_confidence\": decision_service.learned_patterns
        }
        
    except Exception as e:
        logger.error(f\"Error in get_decision_stats: {e}\")
        raise HTTPException(status_code=500, detail=str(e))
