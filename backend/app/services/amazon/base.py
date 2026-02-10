from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class ProductInfo:
    asin: str
    title: str
    price: float
    category: str = "default"

class AmazonClient(ABC):
    @abstractmethod
    async def get_commission_rates(self) -> dict[str, float]:
        ...

    @abstractmethod
    async def resolve_product(self, url_or_asin: str) -> ProductInfo:
        ...

    @abstractmethod
    async def build_affiliate_link(self, asin: str) -> str:
        ...
