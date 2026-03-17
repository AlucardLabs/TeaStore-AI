"""Base classes for workflows."""

from typing import TypedDict, List, Dict, Optional, Any
from pydantic import BaseModel


class WorkflowState(TypedDict, total=False):
    """Base state for all workflows."""
    status: str
    error: Optional[str]
    metadata: Dict[str, Any]


class SearchState(TypedDict, total=False):
    """State for search workflow."""
    # Input
    query: str
    limit: int
    filters: Optional[Dict]

    # Processing
    raw_results: List[Dict]
    filtered_results: List[Dict]
    final_results: List[Dict]

    # Output
    total: int
    query_time_ms: float
    status: str
    error: Optional[str]


class IndexState(TypedDict, total=False):
    """State for indexing workflow."""
    # Input
    batch_size: int

    # Processing
    products: List[Dict]
    current_batch: int
    total_batches: int
    indexed_count: int
    failed_count: int

    # Output
    total_products: int
    duration_seconds: float
    status: str
    error: Optional[str]
