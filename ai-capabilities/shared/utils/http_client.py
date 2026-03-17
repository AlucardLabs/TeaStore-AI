"""HTTP client utilities."""

import httpx
from typing import Optional


class HTTPClient:
    """Async HTTP client wrapper."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        """Initialize HTTP client.

        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
        """
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            follow_redirects=True,
        )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


def get_http_client(base_url: Optional[str] = None, timeout: float = 30.0) -> HTTPClient:
    """Get HTTP client instance.

    Args:
        base_url: Base URL for all requests
        timeout: Request timeout in seconds

    Returns:
        HTTPClient instance
    """
    return HTTPClient(base_url=base_url, timeout=timeout)
