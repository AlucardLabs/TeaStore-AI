"""AI Orchestrator Service - Workflow orchestration with LangChain/LangGraph."""

import sys
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import structlog

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.models import HealthResponse
from shared.config import get_settings
from shared.utils.logging import setup_logging, get_logger

from workflows import SearchWorkflow, IndexWorkflow

# Initialize logging
settings = get_settings()
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)

# Global workflow instances
search_workflow = None
index_workflow = None


class WorkflowSearchRequest(BaseModel):
    """Request model for search workflow."""
    query: str = Field(..., description="Search query", min_length=1, max_length=500)
    limit: int = Field(default=10, description="Maximum results", ge=1, le=100)
    filters: Optional[Dict] = Field(default=None, description="Optional filters")


class WorkflowIndexRequest(BaseModel):
    """Request model for index workflow."""
    batch_size: int = Field(default=32, description="Batch size", ge=1, le=100)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    global search_workflow, index_workflow

    logger.info("Starting AI Orchestrator Service")

    # Initialize workflows
    search_workflow = SearchWorkflow()
    index_workflow = IndexWorkflow()

    logger.info("AI Orchestrator Service started successfully")

    yield

    logger.info("Shutting down AI Orchestrator Service")


# Create FastAPI app
app = FastAPI(
    title="TeaStore AI - Orchestrator Service",
    description="AI workflow orchestration with LangChain/LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="ai-orchestrator",
        version="1.0.0",
        details={
            "langchain_enabled": True,
            "langgraph_enabled": True,
            "workflows_available": ["search", "index"]
        }
    )


@app.post("/workflows/search")
async def execute_search_workflow(request: WorkflowSearchRequest):
    """Execute the search workflow using LangGraph.

    This workflow orchestrates:
    1. Semantic search
    2. Filter application
    3. Result re-ranking

    Args:
        request: Search workflow request

    Returns:
        Search results with metadata
    """
    try:
        logger.info(
            "Search workflow requested",
            query=request.query,
            limit=request.limit
        )

        result = await search_workflow.execute(
            query=request.query,
            limit=request.limit,
            filters=request.filters
        )

        return result

    except Exception as e:
        logger.error("Search workflow failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Search workflow failed: {str(e)}")


@app.post("/workflows/index")
async def execute_index_workflow(request: WorkflowIndexRequest):
    """Execute the indexing workflow using LangGraph.

    This workflow orchestrates:
    1. Fetch products
    2. Trigger indexing

    Args:
        request: Index workflow request

    Returns:
        Indexing results with metadata
    """
    try:
        logger.info(
            "Index workflow requested",
            batch_size=request.batch_size
        )

        result = await index_workflow.execute(
            batch_size=request.batch_size
        )

        return result

    except Exception as e:
        logger.error("Index workflow failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Index workflow failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
