from __future__ import annotations

from .base import AmazonClient, ProductInfo

class LiveAmazonClient(AmazonClient):
    """
    Skeleton for real Amazon integration.

    Real-world notes:
    - Product Advertising API (PA-API) requires AWS SigV4 signing and has strict rate limits.
    - "Fee schedule / commission rates" are often NOT available via PA-API directly; typically
      via Associates UI or report exports. For this assignment, mock is acceptable.
    - Transaction verification also typically happens via report ingestion, not real-time.
    """

    async def get_commission_rates(self) -> dict[str, float]:
        raise NotImplementedError("Implement via Associates report ingestion or other allowed source.")

    async def resolve_product(self, url_or_asin: str) -> ProductInfo:
        raise NotImplementedError("Implement PA-API GetItems (SigV4 signing, retries, rate limits).")

    async def build_affiliate_link(self, asin: str) -> str:
        # Usually affiliate link is just tagged URL.
        raise NotImplementedError
