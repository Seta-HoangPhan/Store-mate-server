from pydantic import BaseModel, field_validator
from validations.phone_validate import phone_validate


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


class LoginSchema(BaseModel):
    phone: str
    password: str

    @field_validator("phone")
    def validate_phone(cls, v):
        return phone_validate(v)

    class Config:
        from_attributes = True


class RefreshTokenSchema(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True
