"""LangChain tools for search operations."""

from typing import List, Dict, Optional
from langchain.tools import tool
import httpx
import structlog

logger = structlog.get_logger(__name__)


@tool
def semantic_search_tool(
    query: str,
    limit: int = 10,
    category: Optional[str] = None,
    max_price_cents: Optional[int] = None
) -> List[Dict]:
    """Search for products using semantic similarity.

    Args:
        query: The search query text
        limit: Maximum number of results to return
        category: Optional category filter (e.g., "Green Tea", "Black Tea")
        max_price_cents: Optional maximum price filter in cents

    Returns:
        List of product dictionaries with scores
    """
    try:
        # Build request
        request_data = {
            "query": query,
            "limit": limit
        }

        # Add filters if provided
        if category or max_price_cents:
            request_data["filters"] = {}
            if category:
                request_data["filters"]["category"] = category
            if max_price_cents:
                request_data["filters"]["max_price_cents"] = max_price_cents

        # Call search service
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                "http://search-service:8001/search",
                json=request_data
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "Semantic search completed",
                    query=query,
                    results=len(data.get("results", []))
                )
                return data.get("results", [])
            else:
                logger.error(
                    "Search failed",
                    status_code=response.status_code,
                    response=response.text
                )
                return []

    except Exception as e:
        logger.error("Search tool error", error=str(e))
        return []


@tool
def similar_products_tool(product_id: int, limit: int = 10) -> List[Dict]:
    """Find products similar to a given product.

    Args:
        product_id: ID of the product to find similar items for
        limit: Maximum number of similar products to return

    Returns:
        List of similar product dictionaries with scores
    """
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"http://search-service:8001/similar/{product_id}",
                params={"limit": limit}
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "Similar products found",
                    product_id=product_id,
                    results=len(data.get("results", []))
                )
                return data.get("results", [])
            else:
                logger.error(
                    "Similar products search failed",
                    status_code=response.status_code
                )
                return []

    except Exception as e:
        logger.error("Similar products tool error", error=str(e))
        return []
