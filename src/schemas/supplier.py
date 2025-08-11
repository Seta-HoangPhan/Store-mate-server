from typing import Optional

from pydantic import EmailStr

from .base import BaseSchemaModel, phone_list_validator


class SupSchema(BaseSchemaModel):
    name: str
    phones: list[str]
    email: Optional[EmailStr] = None
    address: str

    _validate_phones = phone_list_validator()


class PhoneSchema(BaseSchemaModel):
    id: int
    phone: str


class SupResSchema(BaseSchemaModel):
    id: int
    name: str
    phones: list[PhoneSchema]
    email: Optional[EmailStr] = None
    address: str


class UpdatePhoneSchema(BaseSchemaModel):
    id: Optional[int] = None
    phone: str


class UpdateSupSchema(BaseSchemaModel):
    name: Optional[str] = None
    phones: Optional[list[UpdatePhoneSchema]] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    _validate_phones = phone_list_validator()
