from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)


# do not allow deletion of products
class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    thumbnail = Column(String(500))
    last_unit_price = Column(Numeric(10, 2))
    curr_unit_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    purchase_products = relationship(
        "PurchaseProducts", back_populates="product", passive_deletes=True
    )
    order_products = relationship(
        "OrderProduct", back_populates="product", passive_deletes=True
    )


Category.products = relationship(
    "Product", back_populates="category", passive_deletes=True
)
Product.category = relationship("Category", back_populates="products")
