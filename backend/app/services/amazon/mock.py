from __future__ import annotations

import random
import re
from app.core.config import settings
from .base import AmazonClient, ProductInfo

_ASIN_RE = re.compile(r"/dp/([A-Z0-9]{10})|/gp/product/([A-Z0-9]{10})|^([A-Z0-9]{10})$")

class MockAmazonClient(AmazonClient):
    """
    Deterministic-enough mock to demo full flow without Amazon approval.
    """

    async def get_commission_rates(self) -> dict[str, float]:
        return {
            "default": 0.03,
            "electronics": 0.02,
            "books": 0.04,
        }

    async def resolve_product(self, url_or_asin: str) -> ProductInfo:
        s = (url_or_asin or "").strip()
        m = _ASIN_RE.search(s)
        asin = None
        if m:
            asin = next((g for g in (m.group(1), m.group(2), m.group(3)) if g), None)
        asin = asin or "B000000000"

        catalog = {
            "B08N5WRWNW": ("Echo Dot (4th Gen)", 49.99, "electronics"),
            "B09V3KXJPB": ("Fire TV Stick 4K", 59.99, "electronics"),
            "B000000000": ("Demo Product", 19.99, "default"),
        }

        if asin in catalog:
            title, price, cat = catalog[asin]
            return ProductInfo(asin=asin, title=title, price=float(price), category=cat)

        # fallback for random ASINs
        price = round(random.uniform(10, 200), 2)
        return ProductInfo(asin=asin, title=f"Demo Product {asin}", price=price, category="default")

    async def build_affiliate_link(self, asin: str) -> str:
        return f"https://www.amazon.com/dp/{asin}/?tag={settings.AMAZON_ASSOCIATE_TAG}"
