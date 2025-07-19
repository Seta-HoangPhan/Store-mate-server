from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from validations.phone_validate import phone_validate


class AdminSchema(BaseModel):
    phone: str
    email: Optional[EmailStr] = None

    @field_validator("phone")
    def validate_phone(cls, v):
        return phone_validate(v)

    class Config:
        from_attributes = True


class ResendOTPSchema(BaseModel):
    phone: str

    @field_validator("phone")
    def validate_phone(cls, v):
        return phone_validate(v)

    class Config:
        from_attributes = True


class VerifyOTPSchema(BaseModel):
    otp: str
    phone: str

    @field_validator("phone")
    def validate_phone(cls, v):
        return phone_validate(v)

    class Config:
        from_attributes = True


class AdminResponseSchema(BaseModel):
    id: int
    phone: str
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True
