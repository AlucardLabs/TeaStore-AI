"""Track 2 Intelligent API endpoint - LLM-based natural language interface."""

import os
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import httpx
import structlog

from intent.router import IntentRouter

logger = structlog.get_logger(__name__)

# Create API router
router = APIRouter(prefix="/api/v1", tags=["Track 2 - Intelligent API"])

# Get orchestrator service URL from environment
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_SERVICE_URL", "http://ai-orchestrator:8003")

# Initialize intent router (will be created on first use)
intent_router: Optional[IntentRouter] = None


def get_intent_router() -> IntentRouter:
    """Get or create intent router instance."""
    global intent_router
    if intent_router is None:
        intent_router = IntentRouter(model_name="llama3.2")
    return intent_router


class IntelligentRequest(BaseModel):
    """Request model for intelligent endpoint."""
    request: str = Field(
        ...,
        description="Natural language request",
        min_length=1,
        max_length=1000,
        examples=[
            "Show me organic green teas under $20",
            "Find teas similar to Earl Grey",
            "Recommend something for beginners"
        ]
    )


@router.post("/intelligent")
async def intelligent_query(req: IntelligentRequest):
    """Process natural language requests with LLM intent detection.

    Track 2 Intelligent API - Uses LLM to understand intent and route to workflows.
    Enables natural language queries without requiring structured parameters.

    Examples:
    - "Show me organic green teas under $20 from Japan"
    - "Find teas similar to Earl Grey"
    - "Recommend smooth teas for beginners"
    """
    try:
        logger.info("Track 2 intelligent request", request=req.request)

        # Step 1: Analyze intent with LLM
        router_instance = get_intent_router()
        analysis = await router_instance.analyze_request(req.request)

        intent = analysis.get("intent", "SEARCH")
        parameters = analysis.get("parameters", {})

        logger.info(
            "Intent detected",
            intent=intent,
            parameters=parameters
        )

        # Step 2: Route to appropriate workflow
        if intent == "SEARCH":
            # Execute search workflow
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{ORCHESTRATOR_URL}/workflows/search",
                    json={
                        "query": parameters.get("query", req.request),
                        "limit": parameters.get("limit", 10),
                        "filters": parameters.get("filters")
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "intent": intent,
                        "results": result.get("results", []),
                        "total": result.get("total", 0),
                        "query_time_ms": result.get("query_time_ms"),
                        "analysis": analysis
                    }
                else:
                    logger.error(
                        "Workflow execution failed",
                        status_code=response.status_code
                    )
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Workflow failed: {response.text}"
                    )

        elif intent in ["QUESTION", "RECOMMENDATION", "COMPARISON"]:
            # For Phase 3, these fall back to search
            # In Phase 4, they would use specialized workflows/agents
            async with httpx.AsyncClient(timeout=30.0) as client:
                query = parameters.get("query", parameters.get("topic", req.request))
                response = await client.post(
                    f"{ORCHESTRATOR_URL}/workflows/search",
                    json={
                        "query": query,
                        "limit": parameters.get("limit", 10)
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "intent": intent,
                        "message": f"For {intent} queries, showing search results. Full support coming in Phase 4.",
                        "results": result.get("results", []),
                        "total": result.get("total", 0),
                        "analysis": analysis
                    }
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Workflow failed: {response.text}"
                    )

        else:  # CHAT or unknown
            return {
                "intent": intent,
                "message": "Conversational chat support coming in Phase 4. Try a search query.",
                "suggestion": "Example: 'Show me green teas' or 'Find teas under $15'",
                "analysis": analysis
            }

    except httpx.RequestError as e:
        logger.error("Orchestrator request failed", error=str(e))
        raise HTTPException(
            status_code=503,
            detail=f"Orchestrator service unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error("Intelligent query failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Request processing failed: {str(e)}"
        )
