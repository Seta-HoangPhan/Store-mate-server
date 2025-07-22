from typing import Optional

from pydantic import EmailStr

from .base import BaseSchemaModel, phone_validator


class SupSchema(BaseSchemaModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    address: str

    _validate_phone = phone_validator()


class SupResSchema(SupSchema):
    id: int


class UpdateSupSchema(BaseSchemaModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    _validate_phone = phone_validator()
