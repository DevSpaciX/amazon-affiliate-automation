from __future__ import annotations

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    asin: Mapped[str] = mapped_column(String(32), index=True)
    original_url: Mapped[str] = mapped_column(String(2048))
    affiliate_url: Mapped[str] = mapped_column(String(2048))
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    clicks: Mapped[list["Click"]] = relationship(back_populates="link", cascade="all,delete-orphan")
    txs: Mapped[list["Transaction"]] = relationship(back_populates="link", cascade="all,delete-orphan")

class Click(Base):
    __tablename__ = "clicks"

    id: Mapped[int] = mapped_column(primary_key=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"), index=True)
    buyer_id: Mapped[str] = mapped_column(String(64), index=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    link: Mapped["Link"] = relationship(back_populates="clicks")

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"), index=True)
    product_name: Mapped[str] = mapped_column(String(512))

    quantity: Mapped[int] = mapped_column(Integer)
    item_price: Mapped[float] = mapped_column(Float)

    commission_rate: Mapped[float] = mapped_column(Float)  # e.g. 0.03
    affiliate_income: Mapped[float] = mapped_column(Float)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    link: Mapped["Link"] = relationship(back_populates="txs")
