"""Indexing workflow using LangGraph."""

import time
from typing import Dict
from langgraph.graph import StateGraph, END
import httpx
import structlog

from workflows.base import IndexState

logger = structlog.get_logger(__name__)


class IndexWorkflow:
    """LangGraph workflow for product indexing."""

    def __init__(self):
        """Initialize the indexing workflow."""
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(IndexState)

        # Add nodes
        workflow.add_node("fetch_products", self._fetch_products_node)
        workflow.add_node("trigger_indexing", self._trigger_indexing_node)

        # Define edges
        workflow.set_entry_point("fetch_products")
        workflow.add_edge("fetch_products", "trigger_indexing")
        workflow.add_edge("trigger_indexing", END)

        return workflow.compile()

    def _fetch_products_node(self, state: IndexState) -> IndexState:
        """Fetch products from source."""
        try:
            logger.info("Fetching products from mock data")

            # For Phase 2, we just get the count
            # The actual indexing is delegated to the Indexer Service
            with httpx.Client(timeout=60.0) as client:
                response = client.get("http://indexer-service:8002/mock/products")

                if response.status_code == 200:
                    data = response.json()
                    products = data.get("products", [])
                    state["products"] = products
                    state["total_products"] = len(products)
                    state["status"] = "fetched"

                    logger.info("Products fetched", count=len(products))
                else:
                    logger.error("Failed to fetch products", status_code=response.status_code)
                    state["status"] = "failed"
                    state["error"] = f"Failed to fetch products: {response.status_code}"
                    state["products"] = []
                    state["total_products"] = 0

            return state

        except Exception as e:
            logger.error("Fetch products node failed", error=str(e))
            state["status"] = "failed"
            state["error"] = str(e)
            state["products"] = []
            state["total_products"] = 0
            return state

    def _trigger_indexing_node(self, state: IndexState) -> IndexState:
        """Trigger the indexing process."""
        try:
            logger.info("Triggering indexing", product_count=state.get("total_products", 0))

            # Call the indexer service to perform the actual indexing
            with httpx.Client(timeout=120.0) as client:
                response = client.post("http://indexer-service:8002/index/full")

                if response.status_code == 200:
                    data = response.json()
                    state["indexed_count"] = data.get("indexed_products", 0)
                    state["failed_count"] = data.get("failed_products", 0)
                    state["duration_seconds"] = data.get("duration_seconds", 0)
                    state["status"] = data.get("status", "completed")

                    logger.info(
                        "Indexing completed",
                        indexed=state["indexed_count"],
                        failed=state["failed_count"]
                    )
                else:
                    logger.error("Indexing failed", status_code=response.status_code)
                    state["status"] = "failed"
                    state["error"] = f"Indexing failed: {response.status_code}"
                    state["indexed_count"] = 0
                    state["failed_count"] = state.get("total_products", 0)

            return state

        except Exception as e:
            logger.error("Trigger indexing node failed", error=str(e))
            state["status"] = "failed"
            state["error"] = str(e)
            state["indexed_count"] = 0
            state["failed_count"] = state.get("total_products", 0)
            return state

    async def execute(self, batch_size: int = 32) -> Dict:
        """Execute the indexing workflow.

        Args:
            batch_size: Batch size for processing

        Returns:
            Indexing results with metadata
        """
        start_time = time.time()

        try:
            logger.info("Starting indexing workflow with mock data")

            # Initialize state
            initial_state: IndexState = {
                "batch_size": batch_size,
                "products": [],
                "total_products": 0,
                "indexed_count": 0,
                "failed_count": 0,
                "status": "pending"
            }

            # Execute workflow
            final_state = await self.graph.ainvoke(initial_state)

            # Calculate timing
            duration_seconds = time.time() - start_time

            # Build response
            response = {
                "status": final_state.get("status", "unknown"),
                "total_products": final_state.get("total_products", 0),
                "indexed_products": final_state.get("indexed_count", 0),
                "failed_products": final_state.get("failed_count", 0),
                "duration_seconds": round(duration_seconds, 2),
                "error": final_state.get("error")
            }

            logger.info(
                "Indexing workflow completed",
                total=response["total_products"],
                indexed=response["indexed_products"],
                failed=response["failed_products"],
                duration=response["duration_seconds"]
            )

            return response

        except Exception as e:
            logger.error("Indexing workflow failed", error=str(e))
            return {
                "status": "failed",
                "total_products": 0,
                "indexed_products": 0,
                "failed_products": 0,
                "duration_seconds": round(time.time() - start_time, 2),
                "error": str(e)
            }
