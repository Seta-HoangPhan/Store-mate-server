from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from validations.decimal_validate import decimal_validate


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
        return decimal_validate(v)

    class Config:
        from_attributes = True


class UpdateProductSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    last_unit_price: Optional[Decimal] = Field(default=None, gt=0)
    curr_unit_price: Optional[Decimal] = Field(default=None, gt=0)
    selling_price: Optional[Decimal] = Field(default=None, gt=0)
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None

    @field_validator("last_unit_price", "curr_unit_price", "selling_price")
    def validate_decimal(cls, v: Optional[Decimal]):
        return decimal_validate(v)

    class Config:
        from_attributes = True


class PartialCategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    thumbnail: Optional[str] = None
    last_unit_price: Optional[float] = None
    curr_unit_price: float
    selling_price: Optional[float] = None
    stock_quantity: int
    category: Optional[PartialCategorySchema] = None

    class Config:
        from_attributes = True
