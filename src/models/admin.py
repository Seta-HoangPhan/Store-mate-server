from sqlalchemy import Column, Integer, String
from .base import Base, TimestampMixin


class Admin(Base, TimestampMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)
