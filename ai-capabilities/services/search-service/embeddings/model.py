"""Embedding model using sentence-transformers."""

from typing import List
from sentence_transformers import SentenceTransformer
import torch


class EmbeddingModel:
    """Wrapper for sentence-transformers embedding model."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding model.

        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to encode

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        if not texts:
            return []

        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True  # Normalize for cosine similarity
        )

        # Convert numpy arrays to lists
        return [emb.tolist() for emb in embeddings]

    def encode_single(self, text: str) -> List[float]:
        """Generate embedding for a single text.

        Args:
            text: Text string to encode

        Returns:
            Embedding vector as a list of floats
        """
        embeddings = self.encode([text])
        return embeddings[0] if embeddings else []

    def get_dimension(self) -> int:
        """Get the dimensionality of the embeddings.

        Returns:
            Embedding dimension
        """
        return self.dimension

    def get_model_name(self) -> str:
        """Get the name of the model.

        Returns:
            Model name
        """
        return self.model_name


# Global model instance
_embedding_model: EmbeddingModel = None


def get_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingModel:
    """Get or create the global embedding model instance.

    Args:
        model_name: Name of the model to use

    Returns:
        EmbeddingModel instance
    """
    global _embedding_model

    if _embedding_model is None or _embedding_model.get_model_name() != model_name:
        _embedding_model = EmbeddingModel(model_name)

    return _embedding_model
