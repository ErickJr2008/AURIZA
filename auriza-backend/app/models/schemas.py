"""
Data models for AURIZA
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request model"""
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None
    autonomy_override: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    action: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    executed: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)


class VoiceRequest(BaseModel):
    """Voice input request"""
    user_id: str
    audio_data: bytes
    language: str = "es"


class VoiceResponse(BaseModel):
    """Voice response model"""
    text: str
    audio_url: Optional[str] = None
    confidence: float


class MemoryEntry(BaseModel):
    """Memory entry model"""
    user_id: str
    content: str
    memory_type: str  # "short_term" or "long_term"
    tags: List[str] = []
    importance: int = Field(default=1, ge=1, le=10)
    created_at: datetime = Field(default_factory=datetime.now)


class UserContext(BaseModel):
    """User context model"""
    user_id: str
    preferences: Dict[str, Any] = {}
    learned_patterns: Dict[str, Any] = {}
    autonomy_level: str = "assisted"
    last_interaction: Optional[datetime] = None


class Decision(BaseModel):
    """Decision model for autonomous actions"""
    user_id: str
    intent: str
    action: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    autonomy_level: str
    parameters: Dict[str, Any] = {}
    requires_confirmation: bool = True


class IntentAnalysis(BaseModel):
    """Intent analysis result"""
    original_text: str
    detected_intent: str
    confidence: float
    entities: Dict[str, List[str]] = {}
    requires_action: bool
    suggested_action: Optional[str] = None
