from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class Purchase(Base, TimestampMixin):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(
        Integer, ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=False
    )
    total_amount = Column(Numeric(scale=2), nullable=False)

    supplier = relationship("Supplier", back_populates="purchases")
    purchase_products = relationship(
        "PurchaseProduct", back_populates="purchase", cascade="all, delete"
    )


class PurchaseProduct(Base, TimestampMixin):
    __tablename__ = "purchase_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(
        Integer, ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    unit_price = Column(Numeric(scale=2), nullable=False)
    discount = Column(Numeric(5, 2), default=0.00)
    purchase_quantity = Column(Integer, nullable=False)

    purchase = relationship("Purchase", back_populates="purchase_products")
    product = relationship("Product", back_populates="purchase_products")
