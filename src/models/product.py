from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    products = relationship("Product", back_populates="category", passive_deletes=True)


# do not allow deletion of products
class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    thumbnail = Column(String(500))
    thumbnail_id = Column(String, unique=True)
    unit_price = Column(Numeric(scale=2), nullable=False)
    selling_price = Column(Numeric(scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    category = relationship("Category", back_populates="products")
    purchase_products = relationship(
        "PurchaseProduct", back_populates="product", passive_deletes=True
    )
    order_products = relationship(
        "OrderProduct", back_populates="product", passive_deletes=True
    )
