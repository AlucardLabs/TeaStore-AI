"""Vector search using Qdrant."""

from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, Range
import structlog

logger = structlog.get_logger(__name__)


class VectorSearch:
    """Vector search client for Qdrant."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "products",
        vector_dimension: int = 384
    ):
        """Initialize vector search client.

        Args:
            host: Qdrant host
            port: Qdrant port
            collection_name: Name of the collection
            vector_dimension: Dimension of the vectors
        """
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.vector_dimension = vector_dimension
        self.client = QdrantClient(host=host, port=port)

        logger.info(
            "Initialized vector search client",
            host=host,
            port=port,
            collection=collection_name
        )

    def ensure_collection(self) -> bool:
        """Ensure the collection exists, create if needed.

        Returns:
            True if collection exists or was created
        """
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                logger.info("Creating collection", collection=self.collection_name)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_dimension,
                        distance=Distance.COSINE
                    )
                )
                logger.info("Collection created", collection=self.collection_name)
            else:
                logger.info("Collection exists", collection=self.collection_name)

            return True

        except Exception as e:
            logger.error("Failed to ensure collection", error=str(e))
            return False

    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict] = None,
        score_threshold: float = 0.0
    ) -> List[Dict]:
        """Search for similar vectors.

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            filters: Optional filters (category, price, etc.)
            score_threshold: Minimum similarity score

        Returns:
            List of search results with scores and payloads
        """
        try:
            # Build Qdrant filters
            qdrant_filter = self._build_filter(filters) if filters else None

            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=qdrant_filter,
                score_threshold=score_threshold
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                })

            logger.info(
                "Search completed",
                results_count=len(results),
                limit=limit,
                has_filters=filters is not None
            )

            return results

        except Exception as e:
            logger.error("Search failed", error=str(e))
            return []

    def _build_filter(self, filters: Dict) -> Optional[Filter]:
        """Build Qdrant filter from search filters.

        Args:
            filters: Filter dictionary

        Returns:
            Qdrant Filter object
        """
        conditions = []

        # Category filter
        if filters.get("category"):
            conditions.append(
                FieldCondition(
                    key="category_name",
                    match=MatchValue(value=filters["category"])
                )
            )

        if filters.get("category_id"):
            conditions.append(
                FieldCondition(
                    key="category_id",
                    match=MatchValue(value=filters["category_id"])
                )
            )

        # Price range filters
        price_range = {}
        if filters.get("min_price_cents") is not None:
            price_range["gte"] = filters["min_price_cents"]
        if filters.get("max_price_cents") is not None:
            price_range["lte"] = filters["max_price_cents"]

        if price_range:
            conditions.append(
                FieldCondition(
                    key="price_cents",
                    range=Range(**price_range)
                )
            )

        # Origin filter
        if filters.get("origin"):
            conditions.append(
                FieldCondition(
                    key="origin",
                    match=MatchValue(value=filters["origin"])
                )
            )

        if not conditions:
            return None

        return Filter(must=conditions)

    def get_collection_info(self) -> Dict:
        """Get information about the collection.

        Returns:
            Collection info dictionary
        """
        try:
            collection = self.client.get_collection(self.collection_name)
            return {
                "name": collection.name,
                "vectors_count": collection.vectors_count,
                "points_count": collection.points_count,
                "status": collection.status
            }
        except Exception as e:
            logger.error("Failed to get collection info", error=str(e))
            return {}
