"""LangChain tool for product details."""

from typing import Optional, Dict, List
from langchain.tools import tool
import httpx
import structlog

logger = structlog.get_logger(__name__)


@tool
def get_product_details_tool(product_id: int) -> Optional[Dict]:
    """Get detailed information about a specific product.

    This searches for the product by ID and returns its full details.

    Args:
        product_id: The ID of the product to retrieve

    Returns:
        Product dictionary if found, None otherwise
    """
    try:
        # Use semantic search to find the product
        # We'll search for a unique product identifier
        with httpx.Client(timeout=30.0) as client:
            # Search with a very high limit to ensure we find it
            response = client.post(
                "http://search-service:8001/search",
                json={"query": f"product {product_id}", "limit": 100}
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                # Find exact match by ID
                for result in results:
                    if result.get("product", {}).get("id") == product_id:
                        logger.info("Product details retrieved", product_id=product_id)
                        return result.get("product")

                logger.warning("Product not found", product_id=product_id)
                return None
            else:
                logger.error(
                    "Failed to retrieve product",
                    status_code=response.status_code
                )
                return None

    except Exception as e:
        logger.error("Product details tool error", error=str(e))
        return None


@tool
def get_products_by_category_tool(category: str, limit: int = 20) -> List[Dict]:
    """Get all products in a specific category.

    Args:
        category: Category name (e.g., "Green Tea", "Black Tea")
        limit: Maximum number of products to return

    Returns:
        List of products in the category
    """
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                "http://search-service:8001/search",
                json={
                    "query": category,
                    "limit": limit,
                    "filters": {"category": category}
                }
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "Products by category retrieved",
                    category=category,
                    count=len(data.get("results", []))
                )
                return data.get("results", [])
            else:
                logger.error("Failed to get products by category", status_code=response.status_code)
                return []

    except Exception as e:
        logger.error("Get products by category tool error", error=str(e))
        return []
