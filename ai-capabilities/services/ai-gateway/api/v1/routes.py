"""Track 1 Direct API endpoints - Fast, no LLM required."""

import os
from typing import Optional, Dict, List
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
import httpx
import structlog

logger = structlog.get_logger(__name__)

# Create API router
router = APIRouter(prefix="/api/v1", tags=["Track 1 - Direct APIs"])

# Get orchestrator service URL from environment
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_SERVICE_URL", "http://ai-orchestrator:8003")
SEARCH_URL = os.getenv("SEARCH_SERVICE_URL", "http://search-service:8001")


class SearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str = Field(..., description="Search query", min_length=1, max_length=500)
    limit: int = Field(default=10, description="Maximum results", ge=1, le=100)
    filters: Optional[Dict] = Field(default=None, description="Optional filters")


class IndexRequest(BaseModel):
    """Request model for indexing."""
    batch_size: int = Field(default=32, description="Batch size", ge=1, le=100)


@router.post("/search")
async def search(request: SearchRequest):
    """Semantic search via orchestrator workflow.

    Track 1 Direct API - Fast path without LLM.
    Executes semantic search using vector similarity.
    """
    try:
        logger.info(
            "Track 1 search requested",
            query=request.query,
            limit=request.limit
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{ORCHESTRATOR_URL}/workflows/search",
                json={
                    "query": request.query,
                    "limit": request.limit,
                    "filters": request.filters
                }
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(
                    "Track 1 search completed",
                    results=result.get("total", 0),
                    query_time_ms=result.get("query_time_ms")
                )
                return result
            else:
                logger.error(
                    "Search workflow failed",
                    status_code=response.status_code,
                    detail=response.text
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Search failed: {response.text}"
                )

    except httpx.RequestError as e:
        logger.error("Search request failed", error=str(e))
        raise HTTPException(status_code=503, detail=f"Orchestrator service unavailable: {str(e)}")


@router.get("/similar/{product_id}")
async def similar_products(
    product_id: int = Path(..., description="Product ID", ge=1)
):
    """Find similar products by ID.

    Track 1 Direct API - Fast path without LLM.
    Uses vector similarity to find related products.
    """
    try:
        logger.info("Track 1 similar products requested", product_id=product_id)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SEARCH_URL}/similar/{product_id}",
                params={"limit": 10}
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(
                    "Track 1 similar products completed",
                    product_id=product_id,
                    results=result.get("total", 0)
                )
                return result
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
            else:
                logger.error(
                    "Similar products failed",
                    status_code=response.status_code,
                    detail=response.text
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Similar products failed: {response.text}"
                )

    except httpx.RequestError as e:
        logger.error("Similar products request failed", error=str(e))
        raise HTTPException(status_code=503, detail=f"Search service unavailable: {str(e)}")


@router.post("/index")
async def trigger_indexing(request: IndexRequest):
    """Trigger product indexing workflow.

    Track 1 Direct API - Fast path without LLM.
    Initiates the indexing process for products.
    """
    try:
        logger.info(
            "Track 1 indexing requested",
            batch_size=request.batch_size
        )

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{ORCHESTRATOR_URL}/workflows/index",
                json={
                    "batch_size": request.batch_size
                }
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(
                    "Track 1 indexing completed",
                    indexed=result.get("indexed_products", 0),
                    duration=result.get("duration_seconds")
                )
                return result
            else:
                logger.error(
                    "Indexing workflow failed",
                    status_code=response.status_code,
                    detail=response.text
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Indexing failed: {response.text}"
                )

    except httpx.RequestError as e:
        logger.error("Indexing request failed", error=str(e))
        raise HTTPException(status_code=503, detail=f"Orchestrator service unavailable: {str(e)}")
