from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from response import err_msg


class ProductSchema(BaseModel):
    name: str
    description: Optional[str] = None
    last_unit_price: Optional[Decimal] = Field(default=None, gt=0)
    curr_unit_price: Decimal = Field(..., gt=0)
    selling_price: Optional[Decimal] = Field(default=None, gt=0)
    stock_quantity: int
    category_id: Optional[int] = None

    @field_validator("last_unit_price", "curr_unit_price", "selling_price")
    def validate_decimal(cls, v: Optional[Decimal]):
        if v is None:
            return v

        rounded = v.quantize(Decimal("0.01"))  # Enforce 2 decimal places
        # Validate: max 8 digits before decimal, 2 after (total 10)
        sign, digits, exponent = rounded.as_tuple()
        digits_before = len(digits) + exponent if exponent < 0 else len(digits)
        if digits_before > 8:
            raise ValueError(err_msg.INVALID_DECIMAL)

        return rounded

    class Config:
        from_attributes = True


class ProductResponseSchema(ProductSchema):
    id: int
    thumbnail: Optional[str] = None
