"""
🧠 DECISION SERVICE - The brain of AURIZA's autonomy

This service handles:
- Intent recognition
- Context evaluation
- Decision-making
- Action execution (or request for confirmation)
- Learning from decisions
"""

import logging
from typing import Dict, Optional, Any, Tuple
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Types of intents AURIZA can recognize"""
    INFORMATION = "information"  # "¿Qué hora es?"
    ACTION = "action"  # "Abre Spotify"
    AUTOMATION = "automation"  # "Crea una rutina"
    DECISION = "decision"  # "¿Debería...?"
    QUERY = "query"  # "¿Dónde está...?"
    CONTROL = "control"  # "Sube el volumen"
    LEARNING = "learning"  # "Recuerda que..."


class DecisionService:
    """
    Advanced decision-making service for AURIZA
    
    Evaluates context, confidence, and autonomy level to decide:
    - Whether to execute immediately (autonomous)
    - Ask for permission (assisted)
    - Just inform (manual)
    """
    
    def __init__(self, autonomy_level: str = "assisted"):
        self.autonomy_level = autonomy_level
        self.decision_history: Dict[str, Any] = {}
        self.learned_patterns: Dict[str, float] = {}
        
    async def analyze_and_decide(
        self,
        user_input: str,
        user_context: Dict[str, Any],
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main decision-making pipeline
        
        Flow:
        Input → Intent Detection → Context Evaluation → 
        Confidence Calculation → Action Decision
        """
        
        # Step 1: Intent Detection
        intent, confidence = await self._detect_intent(user_input, user_context)
        logger.info(f"Detected intent: {intent} (confidence: {confidence})")
        
        # Step 2: Context Evaluation
        context_score = await self._evaluate_context(intent, user_context, user_preferences)
        
        # Step 3: Calculate final confidence
        final_confidence = (confidence + context_score) / 2
        
        # Step 4: Determine action based on autonomy level
        action_decision = self._determine_action(
            intent=intent,
            confidence=final_confidence,
            autonomy_level=self.autonomy_level,
            user_preferences=user_preferences
        )
        
        return {
            "intent": intent.value,
            "confidence": final_confidence,
            "action": action_decision["action"],
            "requires_confirmation": action_decision["requires_confirmation"],
            "suggested_response": action_decision["suggested_response"],
            "context_score": context_score
        }
    
    async def _detect_intent(
        self,
        user_input: str,
        context: Dict[str, Any]
    ) -> Tuple[IntentType, float]:
        """Detect the intent behind user input"""
        
        # Simple intent detection (can be upgraded with ML/NLP)
        user_input_lower = user_input.lower()
        
        # Intent patterns
        intent_patterns = {
            IntentType.ACTION: [
                "abre", "open", "reproduce", "play", "envía", "send",
                "llama", "call", "crea", "create", "inicia", "start"
            ],
            IntentType.CONTROL: [
                "sube", "baja", "apaga", "enciende", "aumenta", "disminuye",
                "volume", "bright", "off", "on"
            ],
            IntentType.INFORMATION: [
                "qué", "what", "cuál", "which", "cómo", "how", "cuándo",
                "when", "dónde", "where", "por qué", "why"
            ],
            IntentType.AUTOMATION: [
                "rutina", "routine", "automatiza", "automatize", "programa",
                "schedule", "configura", "set"
            ],
            IntentType.DECISION: [
                "debería", "should i", "está bien", "is it ok",
                "me recomiendas", "do you recommend"
            ],
            IntentType.LEARNING: [
                "recuerda", "remember", "guarda", "save", "memoriza",
                "memorize", "aprende", "learn"
            ]
        }
        
        # Match patterns
        for intent_type, patterns in intent_patterns.items():
            for pattern in patterns:
                if pattern in user_input_lower:
                    confidence = 0.85 if user_input_lower.startswith(pattern) else 0.70
                    return intent_type, confidence
        
        # Default: information
        return IntentType.QUERY, 0.60
    
    async def _evaluate_context(
        self,
        intent: IntentType,
        user_context: Dict[str, Any],
        user_preferences: Dict[str, Any]
    ) -> float:
        """Evaluate how well the context supports this intent"""
        
        context_score = 0.70  # Base score
        
        # If intent has been used before, increase confidence
        if intent.value in self.learned_patterns:
            context_score += self.learned_patterns[intent.value] * 0.20
        
        # Check user preferences
        if "automation_enabled" in user_preferences:
            if intent == IntentType.AUTOMATION and user_preferences["automation_enabled"]:
                context_score += 0.15
        
        # Check if we have relevant memory
        if user_context.get("has_relevant_memory"):
            context_score += 0.10
        
        return min(context_score, 1.0)
    
    def _determine_action(
        self,
        intent: IntentType,
        confidence: float,
        autonomy_level: str,
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Determine what action to take"""
        
        # Thresholds for decision-making
        HIGH_CONFIDENCE_THRESHOLD = 0.85
        MEDIUM_CONFIDENCE_THRESHOLD = 0.60
        
        # Decision matrix based on autonomy level and confidence
        
        if autonomy_level == "autonomous":
            # 🔴 Autonomous: Execute and report
            if confidence >= HIGH_CONFIDENCE_THRESHOLD:
                return {
                    "action": "execute",
                    "requires_confirmation": False,
                    "suggested_response": "Ya lo hice. Era lo más eficiente."
                }
            elif confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
                return {
                    "action": "execute_with_caution",
                    "requires_confirmation": False,
                    "suggested_response": "Ejecutado. Avísame si no era lo que querías."
                }
            else:
                return {
                    "action": "inform",
                    "requires_confirmation": True,
                    "suggested_response": "Necesito estar más seguro. ¿Es esto lo que querías?"
                }
        
        elif autonomy_level == "assisted":
            # 🔵 Assisted: Suggest and ask
            if confidence >= HIGH_CONFIDENCE_THRESHOLD:
                return {
                    "action": "execute",
                    "requires_confirmation": False,
                    "suggested_response": "Listo. Ejecutado."
                }
            elif confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
                return {
                    "action": "ask_permission",
                    "requires_confirmation": True,
                    "suggested_response": "¿Lo ejecuto?"
                }
            else:
                return {
                    "action": "inform_and_ask",
                    "requires_confirmation": True,
                    "suggested_response": "Necesito más información. ¿Qué específicamente?"
                }
        
        else:  # manual
            # 🟢 Manual: Only respond
            return {
                "action": "inform",
                "requires_confirmation": True,
                "suggested_response": "Aquí está la información que pediste."
            }
    
    async def learn_from_decision(
        self,
        intent: str,
        was_correct: bool,
        feedback: Optional[str] = None
    ):
        """Learn from past decisions"""
        
        if intent not in self.learned_patterns:
            self.learned_patterns[intent] = 0.5
        
        # Adjust pattern confidence
        adjustment = 0.05 if was_correct else -0.05
        self.learned_patterns[intent] = max(0.0, min(1.0, self.learned_patterns[intent] + adjustment))
        
        logger.info(f"Updated pattern confidence for {intent}: {self.learned_patterns[intent]}")
