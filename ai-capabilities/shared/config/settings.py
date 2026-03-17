"""Application settings and configuration."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Vector Database
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_collection: str = "products"
    qdrant_faq_collection: str = "faqs"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"
    vector_dimension: int = 384

    # Search Configuration
    search_top_k: int = 10
    batch_size: int = 32

    # Service URLs
    search_service_url: str = "http://search-service:8001"
    indexer_service_url: str = "http://indexer-service:8002"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
