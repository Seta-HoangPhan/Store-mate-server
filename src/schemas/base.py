from pydantic import BaseModel, field_validator

from validations import validate_discount, validate_phone


class BaseSchemaModel(BaseModel):
    class Config:
        from_attributes = True


def phone_validator():
    return field_validator("phone")(validate_phone)


def discount_validator():
    return field_validator("discount")(validate_discount)
