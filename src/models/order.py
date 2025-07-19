from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    discount = Column(Numeric(10, 2), default=0.00)

    customer = relationship("Customer", back_populates="orders")
    order_products = relationship(
        "OrderProduct", back_populates="order", cascade="all, delete"
    )
