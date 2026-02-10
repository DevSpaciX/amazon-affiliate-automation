import asyncio
import typer

from app.core.db import engine, Base, SessionLocal
from app.services.amazon.mock import MockAmazonClient
from app.services.links import create_link, get_link_by_code
from app.services.transactions import simulate_buy, list_transactions

app = typer.Typer(add_completion=False)

@app.command()
def init_db():
    async def run():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(run())
    typer.echo("DB initialized ✅")

@app.command()
def gen_link(url_or_asin: str):
    async def run():
        amazon = MockAmazonClient()
        async with SessionLocal() as db:
            link = await create_link(db, amazon, url_or_asin)
            typer.echo(f"ASIN: {link.asin}")
            typer.echo(f"AFF:  {link.affiliate_url}")
            typer.echo(f"CODE: {link.code}")
    asyncio.run(run())

@app.command()
def buy(code: str, qty: int = 1):
    async def run():
        amazon = MockAmazonClient()
        async with SessionLocal() as db:
            link = await get_link_by_code(db, code)
            if not link:
                typer.echo("Link not found")
                raise typer.Exit(code=1)

            tx = await simulate_buy(db, amazon, link, qty)
            typer.echo(f"TX: {tx.transaction_id} income=${tx.affiliate_income}")
    asyncio.run(run())

@app.command()
def tx(limit: int = 20):
    async def run():
        async with SessionLocal() as db:
            items = await list_transactions(db, limit=limit)
            for t in items:
                typer.echo(
                    f"{t.transaction_id} | {t.product_name} | qty={t.quantity} | "
                    f"price={t.item_price:.2f} | income={t.affiliate_income:.2f}"
                )
    asyncio.run(run())

if __name__ == "__main__":
    app()
