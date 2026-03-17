"""Indexer Service - Product data loading and indexing."""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import structlog

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.models import HealthResponse, IndexStatus
from shared.config import get_settings
from shared.utils.logging import setup_logging, get_logger

from indexers import ProductIndexer
from mock_data import load_mock_products

# Initialize logging
settings = get_settings()
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)

# Global instances
product_indexer = None
current_index_status = IndexStatus(status="pending")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    global product_indexer

    logger.info("Starting Indexer Service")

    # Initialize product indexer
    product_indexer = ProductIndexer(
        qdrant_host=settings.qdrant_host,
        qdrant_port=settings.qdrant_port,
        search_service_url=settings.search_service_url,
        collection_name=settings.qdrant_collection,
        batch_size=settings.batch_size
    )

    logger.info("Indexer Service started successfully")

    yield

    logger.info("Shutting down Indexer Service")
    if product_indexer:
        product_indexer.close()


# Create FastAPI app
app = FastAPI(
    title="TeaStore AI - Indexer Service",
    description="Product data loading and indexing service",
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
    index_info = product_indexer.get_index_status()

    return HealthResponse(
        status="healthy",
        service="indexer-service",
        version="1.0.0",
        details={
            "data_source": "mock",
            "index": index_info
        }
    )


@app.get("/mock/products")
async def get_mock_products():
    """Get mock product data.

    Returns:
        List of mock products
    """
    try:
        products = load_mock_products()
        logger.info("Loaded mock products", count=len(products))
        return {
            "products": products,
            "total": len(products)
        }
    except Exception as e:
        logger.error("Failed to load mock products", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load mock products: {str(e)}")


@app.post("/index/full", response_model=IndexStatus)
async def index_full_catalog(background_tasks: BackgroundTasks):
    """Trigger full catalog indexing.

    This will load all products and index them to Qdrant.

    Returns:
        Indexing status
    """
    global current_index_status

    if current_index_status.status == "running":
        return current_index_status

    try:
        logger.info("Starting full catalog indexing")

        # Load mock products
        logger.info("Loading mock products")
        products = load_mock_products()

        logger.info("Products loaded", count=len(products))

        # Update status
        current_index_status = IndexStatus(
            status="running",
            total_products=len(products),
            indexed_products=0
        )

        # Index products (synchronous for simplicity in Phase 1)
        result = product_indexer.index_products(products)

        # Update final status
        current_index_status = IndexStatus(
            status=result["status"],
            total_products=result["total_products"],
            indexed_products=result["indexed_products"],
            failed_products=result["failed_products"],
            duration_seconds=result.get("duration_seconds"),
            error=result.get("error")
        )

        logger.info("Indexing completed", status=current_index_status.status)

        return current_index_status

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Indexing failed", error=str(e))
        current_index_status = IndexStatus(
            status="failed",
            total_products=0,
            indexed_products=0,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")


@app.get("/index/status", response_model=IndexStatus)
async def get_index_status():
    """Get current indexing status.

    Returns:
        Current indexing status
    """
    return current_index_status


@app.post("/index/product/{product_id}")
async def index_single_product(product_id: int):
    """Index a single product.

    Args:
        product_id: ID of the product to index

    Returns:
        Success message
    """
    try:
        logger.info("Indexing single product", product_id=product_id)

        # Load mock products
        products = load_mock_products()

        # Find the product
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        # Index it
        result = product_indexer.index_products([product])

        if result["indexed_products"] == 1:
            logger.info("Product indexed successfully", product_id=product_id)
            return {"status": "success", "product_id": product_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to index product")

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to index product", product_id=product_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to index product: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
