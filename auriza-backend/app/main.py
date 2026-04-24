"""
🚀 AURIZA - Main FastAPI Application
Adaptive Unified Responsive Intelligent Zenith Assistant
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

# Import routes
from app.routes import chat, voice, decisions
from app.core.config import get_settings
from app.core.personality import personality, AURIZA_PERSONALITY

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('auriza.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=\"AURIZA\",
    description=\"Advanced Virtual Intelligence Assistant\",
    version=\"1.0.0\"
)

# Settings
settings = get_settings()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"*\"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)


# Health check
@app.get(\"/health\")
async def health_check():
    \"\"\"Health check endpoint\"\"\"
    return {
        \"status\": \"healthy\",
        \"agent\": \"AURIZA\",
        \"version\": \"1.0.0\"
    }


@app.get(\"/info\")
async def info():
    \"\"\"Get AURIZA information\"\"\"
    return {
        \"name\": \"AURIZA\",
        \"full_name\": \"Adaptive Unified Responsive Intelligent Zenith Assistant\",
        \"version\": \"1.0.0\",
        \"personality\": \"Direct, Intelligent, Confident, Slightly Humane\",
        \"autonomy_level\": settings.decision_autonomy_level,
        \"language\": settings.language,
        \"capabilities\": [
            \"Natural Language Processing\",
            \"Conversational AI\",
            \"Voice Recognition\",
            \"Autonomous Decision Making\",
            \"Memory Management\",
            \"Pattern Learning\",
            \"Mobile Control\"
        ]
    }


# Include routers
app.include_router(chat.router)
app.include_router(voice.router)
app.include_router(decisions.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    \"\"\"Handle uncaught exceptions\"\"\"
    logger.error(f\"Unhandled exception: {exc}\")
    return JSONResponse(
        status_code=500,
        content={
            \"error\": \"Internal server error\",
            \"message\": str(exc) if settings.debug else \"An error occurred\"
        }
    )


# Startup event
@app.on_event(\"startup\")
async def startup_event():
    \"\"\"Initialize services on startup\"\"\"
    logger.info(\"=\"*50)
    logger.info(\"🚀 AURIZA Starting Up\")
    logger.info(\"=\"*50)
    logger.info(f\"Environment: {settings.environment}\")
    logger.info(f\"Debug: {settings.debug}\")
    logger.info(f\"Language: {settings.language}\")
    logger.info(f\"AI Model: {settings.ai_model}\")
    logger.info(f\"Autonomy Level: {settings.decision_autonomy_level}\")
    logger.info(\"=\"*50)


# Shutdown event
@app.on_event(\"shutdown\")
async def shutdown_event():
    \"\"\"Cleanup on shutdown\"\"\"
    logger.info(\"🛑 AURIZA Shutting Down\")


if __name__ == \"__main__\":
    import uvicorn
    
    uvicorn.run(
        \"app.main:app\",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
