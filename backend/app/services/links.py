from __future__ import annotations

import secrets
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link
from app.services.amazon.base import AmazonClient

def _make_code() -> str:
    # short, url-safe, human-friendly
    return secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:10]

async def create_link(db: AsyncSession, amazon: AmazonClient, url_or_asin: str) -> Link:
    product = await amazon.resolve_product(url_or_asin)
    affiliate_url = await amazon.build_affiliate_link(product.asin)

    link = Link(
        asin=product.asin,
        original_url=url_or_asin,
        affiliate_url=affiliate_url,
        code=_make_code(),
    )
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link

async def get_link_by_code(db: AsyncSession, code: str) -> Link | None:
    res = await db.execute(select(Link).where(Link.code == code))
    return res.scalar_one_or_none()
