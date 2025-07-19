from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


# do not allow deletion of customers
class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)

    orders = relationship("Order", back_populates="customer", cascade="all, delete")
