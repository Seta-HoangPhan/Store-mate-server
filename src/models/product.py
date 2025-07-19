from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


# do not allow deletion of products
class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    last_unit_price = Column(Numeric(10, 2), nullable=False)
    curr_unit_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )

    category = relationship("Category", back_populates="products")
    purchase_products = relationship(
        "PurchaseProducts", back_populates="product", cascade="all, delete"
    )
    order_products = relationship(
        "OrderProduct", back_populates="product", cascade="all, delete"
    )
