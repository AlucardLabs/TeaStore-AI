"""AI Gateway Service - Unified API entry point for TeaStore AI."""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import structlog

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.models import HealthResponse
from shared.config import get_settings
from shared.utils.logging import setup_logging, get_logger

# Import API routers
from api.v1.routes import router as v1_router
from api.v1.intelligent import router as intelligent_router

# Initialize logging
settings = get_settings()
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    logger.info("Starting AI Gateway Service")

    # Initialize services
    logger.info("AI Gateway Service started successfully")

    yield

    logger.info("Shutting down AI Gateway Service")


# Create FastAPI app
app = FastAPI(
    title="TeaStore AI - Gateway Service",
    description="Unified API entry point with direct and intelligent endpoints",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(v1_router)
app.include_router(intelligent_router)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with Ollama status."""
    # Check if Ollama is available
    ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
    ollama_available = False

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{ollama_url}/api/tags")
            ollama_available = response.status_code == 200
    except:
        ollama_available = False

    return HealthResponse(
        status="healthy",
        service="ai-gateway",
        version="1.0.0",
        details={
            "track_1_enabled": True,
            "track_2_enabled": ollama_available,
            "ollama_status": "available" if ollama_available else "unavailable",
            "api_version": "v1"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
