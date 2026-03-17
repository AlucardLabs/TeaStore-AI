"""Search workflow using LangGraph."""

import time
from typing import Dict, List
from langgraph.graph import StateGraph, END
import structlog

from workflows.base import SearchState
from tools.search_tool import semantic_search_tool
from tools.filter_tool import filter_products_tool

logger = structlog.get_logger(__name__)


class SearchWorkflow:
    """LangGraph workflow for semantic search with filtering and re-ranking."""

    def __init__(self):
        """Initialize the search workflow."""
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(SearchState)

        # Add nodes
        workflow.add_node("search", self._search_node)
        workflow.add_node("apply_filters", self._apply_filters_node)
        workflow.add_node("rerank", self._rerank_node)

        # Define edges
        workflow.set_entry_point("search")
        workflow.add_edge("search", "apply_filters")
        workflow.add_edge("apply_filters", "rerank")
        workflow.add_edge("rerank", END)

        return workflow.compile()

    def _search_node(self, state: SearchState) -> SearchState:
        """Execute semantic search."""
        try:
            logger.info(
                "Executing search node",
                query=state["query"],
                limit=state.get("limit", 10)
            )

            # Call search tool
            results = semantic_search_tool.invoke({
                "query": state["query"],
                "limit": state.get("limit", 10),
                "category": state.get("filters", {}).get("category") if state.get("filters") else None,
                "max_price_cents": state.get("filters", {}).get("max_price_cents") if state.get("filters") else None
            })

            state["raw_results"] = results
            state["status"] = "search_completed"

            logger.info("Search node completed", results_count=len(results))

            return state

        except Exception as e:
            logger.error("Search node failed", error=str(e))
            state["status"] = "failed"
            state["error"] = str(e)
            state["raw_results"] = []
            return state

    def _apply_filters_node(self, state: SearchState) -> SearchState:
        """Apply additional filters to search results."""
        try:
            results = state.get("raw_results", [])

            # If no additional filters needed, skip
            filters = state.get("filters", {})
            if not filters or not results:
                state["filtered_results"] = results
                logger.info("No additional filters to apply")
                return state

            logger.info("Applying filters", filters=filters)

            # Apply filters using the tool
            filtered = filter_products_tool.invoke({
                "products": results,
                "category": filters.get("category"),
                "min_price_cents": filters.get("min_price_cents"),
                "max_price_cents": filters.get("max_price_cents"),
                "origin": filters.get("origin"),
                "min_score": filters.get("min_score")
            })

            state["filtered_results"] = filtered
            logger.info("Filters applied", filtered_count=len(filtered))

            return state

        except Exception as e:
            logger.error("Filter node failed", error=str(e))
            # On error, pass through unfiltered results
            state["filtered_results"] = state.get("raw_results", [])
            return state

    def _rerank_node(self, state: SearchState) -> SearchState:
        """Re-rank results based on business logic."""
        try:
            results = state.get("filtered_results", [])

            if not results:
                state["final_results"] = []
                state["total"] = 0
                return state

            logger.info("Re-ranking results", count=len(results))

            # Re-ranking strategy:
            # 1. Boost products with higher scores
            # 2. Boost products in exact category match
            # 3. Boost products within price preferences

            reranked = []
            for result in results:
                score = result.get("score", 0)
                product = result.get("product", {})

                # Apply boosts
                boost = 0.0

                # Exact category match boost
                if state.get("filters", {}).get("category"):
                    if product.get("category_name") == state["filters"]["category"]:
                        boost += 0.1

                # Price preference boost (favor mid-range)
                price = product.get("price_cents", 0)
                if 1000 <= price <= 2500:
                    boost += 0.05

                # Apply boost
                final_score = min(score + boost, 1.0)

                reranked.append({
                    **result,
                    "score": final_score
                })

            # Sort by final score
            reranked.sort(key=lambda x: x.get("score", 0), reverse=True)

            # Apply limit
            limit = state.get("limit", 10)
            reranked = reranked[:limit]

            state["final_results"] = reranked
            state["total"] = len(reranked)
            state["status"] = "completed"

            logger.info("Re-ranking completed", final_count=len(reranked))

            return state

        except Exception as e:
            logger.error("Rerank node failed", error=str(e))
            # On error, return filtered results without re-ranking
            state["final_results"] = state.get("filtered_results", [])
            state["total"] = len(state["final_results"])
            return state

    async def execute(self, query: str, limit: int = 10, filters: Dict = None) -> Dict:
        """Execute the search workflow.

        Args:
            query: Search query
            limit: Maximum results
            filters: Optional filters

        Returns:
            Search results with metadata
        """
        start_time = time.time()

        try:
            logger.info("Starting search workflow", query=query, limit=limit)

            # Initialize state
            initial_state: SearchState = {
                "query": query,
                "limit": limit,
                "filters": filters or {},
                "raw_results": [],
                "filtered_results": [],
                "final_results": [],
                "total": 0,
                "status": "pending"
            }

            # Execute workflow
            final_state = await self.graph.ainvoke(initial_state)

            # Calculate timing
            query_time_ms = (time.time() - start_time) * 1000

            # Build response
            response = {
                "results": final_state.get("final_results", []),
                "total": final_state.get("total", 0),
                "query_time_ms": round(query_time_ms, 2),
                "status": final_state.get("status", "unknown"),
                "error": final_state.get("error")
            }

            logger.info(
                "Search workflow completed",
                query=query,
                results=response["total"],
                time_ms=response["query_time_ms"]
            )

            return response

        except Exception as e:
            logger.error("Search workflow failed", error=str(e))
            return {
                "results": [],
                "total": 0,
                "query_time_ms": round((time.time() - start_time) * 1000, 2),
                "status": "failed",
                "error": str(e)
            }
