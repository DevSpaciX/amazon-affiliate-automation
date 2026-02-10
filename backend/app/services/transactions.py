from __future__ import annotations

import uuid
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link, Transaction
from app.services.amazon.base import AmazonClient

async def list_transactions(db: AsyncSession, limit: int = 200) -> list[Transaction]:
    res = await db.execute(select(Transaction).order_by(desc(Transaction.created_at)).limit(limit))
    return list(res.scalars().all())

async def simulate_buy(db: AsyncSession, amazon: AmazonClient, link: Link, quantity: int) -> Transaction:
    product = await amazon.resolve_product(link.asin)
    rates = await amazon.get_commission_rates()
    rate = rates.get(product.category, rates.get("default", 0.03))

    item_price = float(product.price)
    affiliate_income = round(item_price * int(quantity) * float(rate), 2)

    tx = Transaction(
        transaction_id=str(uuid.uuid4()),
        link_id=link.id,
        product_name=product.title,
        quantity=int(quantity),
        item_price=item_price,
        commission_rate=float(rate),
        affiliate_income=affiliate_income,
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx
