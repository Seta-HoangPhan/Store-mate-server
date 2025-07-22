from typing import Optional

from pydantic import EmailStr

from .base import BaseSchemaModel, phone_validator


class AdminSchema(BaseSchemaModel):
    phone: str
    email: Optional[EmailStr] = None

    _validate_phone = phone_validator()


class AdminResponseSchema(BaseSchemaModel):
    id: int
    phone: str
    email: Optional[EmailStr] = None


class DeleteAdminSchema(BaseSchemaModel):
    phone: str

    _validate_phone = phone_validator()
