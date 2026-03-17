"""Batch processing utilities for indexing."""

from typing import List, TypeVar, Iterator

T = TypeVar('T')


class BatchProcessor:
    """Utility for processing items in batches."""

    @staticmethod
    def create_batches(items: List[T], batch_size: int) -> Iterator[List[T]]:
        """Split a list into batches.

        Args:
            items: List of items to batch
            batch_size: Size of each batch

        Yields:
            Batches of items
        """
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]
