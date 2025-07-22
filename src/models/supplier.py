from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    address = Column(String(255), nullable=False)

    purchases = relationship(
        "Purchase", back_populates="supplier", passive_deletes=True
    )
