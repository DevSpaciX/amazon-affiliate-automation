from pydantic import BaseModel, Field

class LinkCreateIn(BaseModel):
    url_or_asin: str = Field(..., examples=["B08N5WRWNW", "https://www.amazon.com/dp/B08N5WRWNW"])

class LinkOut(BaseModel):
    asin: str
    affiliate_url: str
    redirect_url: str

class CommissionRateOut(BaseModel):
    category: str
    rate: float

class SimulateBuyIn(BaseModel):
    link_code: str
    buyer_id: str = "demo-buyer"
    quantity: int = 1

class TransactionOut(BaseModel):
    transaction_id: str
    product_name: str
    quantity: int
    item_price: float
    affiliate_income: float

class TransactionsTableOut(BaseModel):
    items: list[TransactionOut]
