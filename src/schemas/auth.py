from .base import BaseSchemaModel, phone_validator


class ResendOTPSchema(BaseSchemaModel):
    phone: str

    _validate_phone = phone_validator()


class VerifyOTPSchema(BaseSchemaModel):
    otp: str
    phone: str

    _validate_phone = phone_validator()


class LoginSchema(BaseSchemaModel):
    phone: str
    password: str

    _validate_phone = phone_validator()


class RefreshTokenSchema(BaseSchemaModel):
    refresh_token: str

    class Config:
        from_attributes = True
