from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.models import Click
from app.schemas import (
    LinkCreateIn, LinkOut,
    CommissionRateOut,
    SimulateBuyIn,
    TransactionsTableOut,
    TransactionOut,
)
from app.services.amazon import MockAmazonClient, LiveAmazonClient
from app.services.links import create_link, get_link_by_code
from app.services.transactions import simulate_buy, list_transactions

router = APIRouter()

def get_amazon_client():
    if settings.AMAZON_MODE == "live":
        return LiveAmazonClient()
    return MockAmazonClient()

@router.get("/api/health")
async def health():
    return {"ok": True, "mode": settings.AMAZON_MODE}

@router.get("/api/commission-rates", response_model=list[CommissionRateOut])
async def commission_rates():
    amazon = get_amazon_client()
    rates = await amazon.get_commission_rates()
    return [{"category": k, "rate": v} for k, v in rates.items()]

@router.post("/api/links", response_model=LinkOut)
async def create_affiliate_link(payload: LinkCreateIn, db: AsyncSession = Depends(get_db)):
    amazon = get_amazon_client()
    link = await create_link(db, amazon, payload.url_or_asin)

    return LinkOut(
        asin=link.asin,
        affiliate_url=link.affiliate_url,
        redirect_url=f"{settings.PUBLIC_BASE_URL}/r/{link.code}",
    )

@router.get("/r/{code}")
async def redirect(code: str, request: Request, db: AsyncSession = Depends(get_db)):
    link = await get_link_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    buyer_id = request.query_params.get("buyer", "anon")
    ua = request.headers.get("user-agent")

    click = Click(
        link_id=link.id,
        buyer_id=buyer_id[:64],
        user_agent=(ua[:512] if ua else None),
    )
    db.add(click)
    await db.commit()

    return RedirectResponse(url=link.affiliate_url, status_code=302)

@router.post("/api/simulate-buy", response_model=TransactionOut)
async def simulate_buy_api(payload: SimulateBuyIn, db: AsyncSession = Depends(get_db)):
    amazon = get_amazon_client()
    link = await get_link_by_code(db, payload.link_code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    tx = await simulate_buy(db, amazon, link, payload.quantity)
    return TransactionOut(
        transaction_id=tx.transaction_id,
        product_name=tx.product_name,
        quantity=tx.quantity,
        item_price=tx.item_price,
        affiliate_income=tx.affiliate_income,
    )

@router.get("/api/transactions", response_model=TransactionsTableOut)
async def transactions(db: AsyncSession = Depends(get_db)):
    items = await list_transactions(db)
    return TransactionsTableOut(
        items=[
            TransactionOut(
                transaction_id=t.transaction_id,
                product_name=t.product_name,
                quantity=t.quantity,
                item_price=t.item_price,
                affiliate_income=t.affiliate_income,
            )
            for t in items
        ]
    )
