"""Search Service - Embedding generation and vector search."""

import sys
import time
from pathlib import Path
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import structlog

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.models import SearchRequest, SearchResponse, SearchResult, Product, HealthResponse
from shared.models.search import EmbeddingRequest, EmbeddingResponse
from shared.config import get_settings
from shared.utils.logging import setup_logging, get_logger

from embeddings import get_embedding_model
from search import VectorSearch

# Initialize logging
settings = get_settings()
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)

# Global instances
embedding_model = None
vector_search = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    global embedding_model, vector_search

    logger.info("Starting Search Service", model=settings.embedding_model)

    # Initialize embedding model
    embedding_model = get_embedding_model(settings.embedding_model)
    logger.info(
        "Embedding model loaded",
        model=embedding_model.get_model_name(),
        dimension=embedding_model.get_dimension(),
        device=embedding_model.device
    )

    # Initialize vector search
    vector_search = VectorSearch(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        collection_name=settings.qdrant_collection,
        vector_dimension=settings.vector_dimension
    )

    # Ensure collection exists
    vector_search.ensure_collection()

    logger.info("Search Service started successfully")

    yield

    logger.info("Shutting down Search Service")


# Create FastAPI app
app = FastAPI(
    title="TeaStore AI - Search Service",
    description="Embedding generation and semantic search service",
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
    collection_info = vector_search.get_collection_info()

    return HealthResponse(
        status="healthy",
        service="search-service",
        version="1.0.0",
        details={
            "model": embedding_model.get_model_name(),
            "dimension": embedding_model.get_dimension(),
            "collection": collection_info
        }
    )


@app.post("/embed", response_model=EmbeddingResponse)
async def generate_embeddings(request: EmbeddingRequest):
    """Generate embeddings for texts.

    Args:
        request: Embedding request with texts

    Returns:
        Embedding response with vectors
    """
    try:
        logger.info("Generating embeddings", text_count=len(request.texts))

        embeddings = embedding_model.encode(request.texts)

        logger.info("Embeddings generated", count=len(embeddings))

        return EmbeddingResponse(
            embeddings=embeddings,
            dimension=embedding_model.get_dimension(),
            model=embedding_model.get_model_name()
        )

    except Exception as e:
        logger.error("Failed to generate embeddings", error=str(e))
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")


@app.post("/search", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """Perform semantic search.

    Args:
        request: Search request with query and filters

    Returns:
        Search response with results
    """
    try:
        start_time = time.time()

        logger.info(
            "Processing search request",
            query=request.query,
            limit=request.limit,
            has_filters=request.filters is not None
        )

        # Generate query embedding
        query_embedding = embedding_model.encode_single(request.query)

        # Build filters dict
        filters = None
        if request.filters:
            filters = request.filters.model_dump(exclude_none=True)

        # Perform vector search
        search_results = vector_search.search(
            query_vector=query_embedding,
            limit=request.limit,
            filters=filters
        )

        # Convert to search results
        results = []
        for hit in search_results:
            # Create Product from payload
            product = Product(**hit["payload"])
            results.append(
                SearchResult(
                    product=product,
                    score=hit["score"]
                )
            )

        query_time_ms = (time.time() - start_time) * 1000

        logger.info(
            "Search completed",
            query=request.query,
            results_count=len(results),
            query_time_ms=round(query_time_ms, 2)
        )

        return SearchResponse(
            results=results,
            total=len(results),
            query_time_ms=round(query_time_ms, 2)
        )

    except Exception as e:
        logger.error("Search failed", error=str(e), query=request.query)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/similar/{product_id}", response_model=SearchResponse)
async def find_similar(product_id: int, limit: int = 10):
    """Find products similar to a given product.

    Args:
        product_id: ID of the product to find similar items for
        limit: Maximum number of results

    Returns:
        Search response with similar products
    """
    try:
        start_time = time.time()

        logger.info("Finding similar products", product_id=product_id, limit=limit)

        # Get the product from Qdrant
        try:
            points = vector_search.client.retrieve(
                collection_name=vector_search.collection_name,
                ids=[product_id],
                with_vectors=True  # Explicitly request vectors
            )

            if not points:
                raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

            product_vector = points[0].vector

        except Exception as e:
            logger.error("Failed to retrieve product", product_id=product_id, error=str(e))
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        # Search for similar products
        search_results = vector_search.search(
            query_vector=product_vector,
            limit=limit + 1  # +1 to exclude the product itself
        )

        # Filter out the original product and convert to search results
        results = []
        for hit in search_results:
            if hit["payload"]["id"] != product_id:
                product = Product(**hit["payload"])
                results.append(
                    SearchResult(
                        product=product,
                        score=hit["score"]
                    )
                )

        # Limit to requested number
        results = results[:limit]

        query_time_ms = (time.time() - start_time) * 1000

        logger.info(
            "Similar products found",
            product_id=product_id,
            results_count=len(results),
            query_time_ms=round(query_time_ms, 2)
        )

        return SearchResponse(
            results=results,
            total=len(results),
            query_time_ms=round(query_time_ms, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to find similar products", error=str(e), product_id=product_id)
        raise HTTPException(status_code=500, detail=f"Failed to find similar products: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
