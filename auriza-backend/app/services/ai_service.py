"""
AI Service - Handles LLM integration and response generation
"""

import logging
from typing import Optional, Dict, Any, List
import httpx

logger = logging.getLogger(__name__)


class AIService:
    """
    Integration with LLM providers (OpenAI, local models, etc.)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
    async def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate AI response using LLM
        
        Args:
            user_message: User input
            system_prompt: System prompt (AURIZA personality)
            context: Additional context
            temperature: Creativity level (0-2)
        
        Returns:
            Generated response
        """
        
        # Build messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history (keep last 5 messages for context)
        messages.extend(self.conversation_history[-10:])
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Try OpenAI API if key is available
            if self.api_key:
                response = await self._call_openai_api(messages, temperature)
            else:
                # Fallback: simple response
                response = await self._generate_fallback_response(user_message)
            
            # Store in history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Necesito revisarme. Intenta de nuevo."
    
    async def _call_openai_api(
        self,
        messages: List[Dict[str, str]],
        temperature: float
    ) -> str:
        """Call OpenAI API"""
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    logger.error(f"OpenAI API error: {response.status_code}")
                    return await self._generate_fallback_response(messages[-1]["content"])
                    
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {e}")
                return await self._generate_fallback_response(messages[-1]["content"])
    
    async def _generate_fallback_response(self, user_input: str) -> str:
        """Generate simple response when API is unavailable"""
        
        user_input_lower = user_input.lower()
        
        # Simple pattern matching for common queries
        responses = {
            "hola": "¿Qué necesitas?",
            "quién eres": "Soy AURIZA. Tu asistente inteligente.",
            "qué puedes hacer": "Controlo tu teléfono, entiendo intenciones y aprendo tus hábitos.",
            "gracias": "De nada.",
            "adiós": "Hasta luego.",
        }
        
        for pattern, response in responses.items():
            if pattern in user_input_lower:
                return response
        
        return "Entendido. ¿Qué necesitas que haga?"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def set_model(self, model: str):
        """Change the LLM model"""
        self.model = model
        logger.info(f"Model changed to: {model}")
