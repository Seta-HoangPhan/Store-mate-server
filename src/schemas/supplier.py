from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from validations.phone_validate import phone_validate


class SupplierSchema(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    address: str

    @field_validator("phone")
    def validate_phone(cls, v: str):
        return phone_validate(v)

    class Config:
        from_attributes = True


class SupplierResponseSchema(SupplierSchema):
    id: int


class UpdateSupplierSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    @field_validator("phone")
    def validate_phone(cls, v: str):
        return phone_validate(v)

    class Config:
        from_attributes = True
