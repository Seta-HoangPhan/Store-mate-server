from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class PurchaseProducts(Base, TimestampMixin):
    __tablename__ = "purchase_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(
        Integer, ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("products.id"))
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), default=0.00)
    purchase_quantity = Column(Integer, nullable=False)

    purchase = relationship("Purchase", back_populates="purchase_products")
    product = relationship("Product", back_populates="purchase_products")
