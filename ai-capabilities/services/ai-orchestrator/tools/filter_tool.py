"""LangChain tool for filtering products."""

from typing import List, Dict, Optional
from langchain.tools import tool
import structlog

logger = structlog.get_logger(__name__)


@tool
def filter_products_tool(
    products: List[Dict],
    category: Optional[str] = None,
    min_price_cents: Optional[int] = None,
    max_price_cents: Optional[int] = None,
    origin: Optional[str] = None,
    min_score: Optional[float] = None
) -> List[Dict]:
    """Filter a list of products based on criteria.

    This tool applies business logic filters to product results.

    Args:
        products: List of product dictionaries (with 'product' and 'score' keys)
        category: Filter by category name
        min_price_cents: Minimum price in cents
        max_price_cents: Maximum price in cents
        origin: Filter by origin country
        min_score: Minimum relevance score

    Returns:
        Filtered list of products
    """
    try:
        filtered = products.copy()
        initial_count = len(filtered)

        # Apply category filter
        if category:
            filtered = [
                p for p in filtered
                if p.get("product", {}).get("category_name") == category
            ]
            logger.debug("Category filter applied", remaining=len(filtered))

        # Apply price filters
        if min_price_cents is not None:
            filtered = [
                p for p in filtered
                if p.get("product", {}).get("price_cents", 0) >= min_price_cents
            ]
            logger.debug("Min price filter applied", remaining=len(filtered))

        if max_price_cents is not None:
            filtered = [
                p for p in filtered
                if p.get("product", {}).get("price_cents", float('inf')) <= max_price_cents
            ]
            logger.debug("Max price filter applied", remaining=len(filtered))

        # Apply origin filter
        if origin:
            filtered = [
                p for p in filtered
                if p.get("product", {}).get("origin") == origin
            ]
            logger.debug("Origin filter applied", remaining=len(filtered))

        # Apply score filter
        if min_score is not None:
            filtered = [
                p for p in filtered
                if p.get("score", 0) >= min_score
            ]
            logger.debug("Min score filter applied", remaining=len(filtered))

        logger.info(
            "Products filtered",
            initial_count=initial_count,
            filtered_count=len(filtered),
            filters_applied={
                "category": category,
                "price_range": f"{min_price_cents}-{max_price_cents}" if min_price_cents or max_price_cents else None,
                "origin": origin,
                "min_score": min_score
            }
        )

        return filtered

    except Exception as e:
        logger.error("Filter tool error", error=str(e))
        return products  # Return unfiltered on error
