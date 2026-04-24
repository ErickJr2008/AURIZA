"""
Voice routes - Speech input/output endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import logging

from app.models.schemas import VoiceResponse
from app.services.voice_service import VoiceService

logger = logging.getLogger(__name__)
router = APIRouter(prefix=\"/api/voice\", tags=[\"voice\"])

# Voice service instance
voice_service = VoiceService(language=\"es\")


@router.post(\"/transcribe\")
async def transcribe_audio(file: UploadFile = File(...)) -> VoiceResponse:
    \"\"\"
    Transcribe audio to text (STT)
    
    Upload an audio file and get transcription
    \"\"\"
    
    try:
        # Read file
        audio_data = await file.read()
        
        # Transcribe
        text, confidence = await voice_service.speech_to_text(audio_data)
        
        return VoiceResponse(
            text=text,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f\"Error in transcribe_audio: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(\"/synthesize\")
async def synthesize_speech(text: str, language: Optional[str] = None) -> dict:
    \"\"\"
    Convert text to speech (TTS)
    
    Returns audio as base64
    \"\"\"
    
    try:
        audio_bytes = await voice_service.text_to_speech(text, language)
        
        import base64
        audio_b64 = base64.b64encode(audio_bytes).decode(\"utf-8\")
        
        return {
            \"text\": text,
            \"audio_base64\": audio_b64,
            \"content_type\": \"audio/mp3\"
        }
        
    except Exception as e:
        logger.error(f\"Error in synthesize_speech: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(\"/activate\")
async def activate_listening(user_id: str) -> dict:
    \"\"\"
    Activate listening mode (respond to wake word)
    
    Example wake words: \"Hey Auriza\", \"Auriza\"
    \"\"\"
    
    try:
        return {
            \"status\": \"listening\",
            \"user_id\": user_id,
            \"wake_words\": [\"Hey Auriza\", \"Auriza\"],
            \"language\": voice_service.language
        }
        
    except Exception as e:
        logger.error(f\"Error in activate_listening: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(\"/process-stream\")
async def process_audio_stream(chunk: bytes) -> dict:
    \"\"\"
    Process streaming audio chunks (for continuous listening)
    \"\"\"
    
    try:
        await voice_service.process_audio_chunk(chunk)
        
        return {
            \"status\": \"processing\",
            \"chunk_size\": len(chunk)
        }
        
    except Exception as e:
        logger.error(f\"Error in process_audio_stream: {e}\")
        raise HTTPException(status_code=500, detail=str(e))
