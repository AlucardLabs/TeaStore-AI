"""Product indexing to Qdrant."""

import time
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import httpx
import structlog

from .batch_processor import BatchProcessor

logger = structlog.get_logger(__name__)


class ProductIndexer:
    """Indexes products to Qdrant vector database."""

    def __init__(
        self,
        qdrant_host: str,
        qdrant_port: int,
        search_service_url: str,
        collection_name: str = "products",
        batch_size: int = 32
    ):
        """Initialize product indexer.

        Args:
            qdrant_host: Qdrant host
            qdrant_port: Qdrant port
            search_service_url: URL of the search service for embeddings
            collection_name: Name of the collection
            batch_size: Batch size for processing
        """
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.search_service_url = search_service_url
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.http_client = httpx.Client(timeout=60.0)

        logger.info(
            "Initialized product indexer",
            qdrant_host=qdrant_host,
            search_service=search_service_url,
            batch_size=batch_size
        )

    def index_products(self, products: List[Dict]) -> Dict:
        """Index a list of products to Qdrant.

        Args:
            products: List of product dictionaries

        Returns:
            Indexing statistics
        """
        start_time = time.time()
        indexed_count = 0
        failed_count = 0

        logger.info("Starting product indexing", total_products=len(products))

        try:
            # Process in batches
            batches = list(BatchProcessor.create_batches(products, self.batch_size))

            for batch_idx, batch in enumerate(batches):
                logger.info(
                    "Processing batch",
                    batch=batch_idx + 1,
                    total_batches=len(batches),
                    batch_size=len(batch)
                )

                try:
                    # Generate embeddings for batch
                    texts = [self._create_text_for_embedding(p) for p in batch]

                    embeddings = self._generate_embeddings(texts)

                    if not embeddings:
                        logger.error("Failed to generate embeddings for batch", batch=batch_idx + 1)
                        failed_count += len(batch)
                        continue

                    # Create Qdrant points
                    points = []
                    for i, product in enumerate(batch):
                        point = PointStruct(
                            id=product['id'],  # Use integer ID directly
                            vector=embeddings[i],
                            payload=product
                        )
                        points.append(point)

                    # Upload to Qdrant
                    self.qdrant_client.upsert(
                        collection_name=self.collection_name,
                        points=points
                    )

                    indexed_count += len(batch)
                    logger.info(
                        "Batch indexed successfully",
                        batch=batch_idx + 1,
                        indexed=len(batch)
                    )

                except Exception as e:
                    logger.error(
                        "Batch indexing failed",
                        batch=batch_idx + 1,
                        error=str(e)
                    )
                    failed_count += len(batch)

            duration_seconds = time.time() - start_time

            logger.info(
                "Indexing completed",
                total=len(products),
                indexed=indexed_count,
                failed=failed_count,
                duration_seconds=round(duration_seconds, 2)
            )

            return {
                "status": "completed" if failed_count == 0 else "completed_with_errors",
                "total_products": len(products),
                "indexed_products": indexed_count,
                "failed_products": failed_count,
                "duration_seconds": round(duration_seconds, 2)
            }

        except Exception as e:
            logger.error("Indexing failed", error=str(e))
            return {
                "status": "failed",
                "total_products": len(products),
                "indexed_products": indexed_count,
                "failed_products": failed_count,
                "error": str(e)
            }

    def _create_text_for_embedding(self, product: Dict) -> str:
        """Create text representation of product for embedding.

        Args:
            product: Product dictionary

        Returns:
            Text string for embedding
        """
        # Combine name, description, and category for rich semantic representation
        parts = [
            product.get("name", ""),
            product.get("description", ""),
            product.get("category_name", "")
        ]

        # Add flavor notes if available
        if product.get("flavor_notes"):
            flavor_text = " ".join(product["flavor_notes"])
            parts.append(flavor_text)

        # Add origin if available
        if product.get("origin"):
            parts.append(f"from {product['origin']}")

        return " ".join(parts)

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using the search service.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = self.http_client.post(
                f"{self.search_service_url}/embed",
                json={"texts": texts}
            )

            if response.status_code == 200:
                data = response.json()
                return data["embeddings"]
            else:
                logger.error(
                    "Failed to generate embeddings",
                    status_code=response.status_code,
                    response=response.text
                )
                return []

        except Exception as e:
            logger.error("Error calling search service", error=str(e))
            return []

    def get_index_status(self) -> Dict:
        """Get current index status.

        Returns:
            Status dictionary with collection info
        """
        try:
            collection = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": collection.name,
                "vectors_count": collection.vectors_count,
                "points_count": collection.points_count,
                "status": collection.status.value if hasattr(collection.status, 'value') else str(collection.status)
            }
        except Exception as e:
            logger.error("Failed to get index status", error=str(e))
            return {"error": str(e)}

    def close(self):
        """Close HTTP client."""
        self.http_client.close()
