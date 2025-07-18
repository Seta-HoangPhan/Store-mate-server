from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Purchase(Base, TimestampMixin):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(
        Integer, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    total_amount = Column(Numeric(10, 2), nullable=False)

    supplier = relationship("Supplier", back_populates="purchases")
    purchase_products = relationship(
        "PurchaseProducts", back_populates="purchase", cascade="all, delete"
    )
