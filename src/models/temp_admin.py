from sqlalchemy import Column, Integer, String

from .base import Base, TimestampMixin


class TempAdmin(Base, TimestampMixin):
    __tablename__ = "temp_admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)
    otp = Column(String(6), nullable=False)
    expiration = Column(
        Integer, nullable=False, default=2
    )  # Timestamp for OTP expiration by minutes
