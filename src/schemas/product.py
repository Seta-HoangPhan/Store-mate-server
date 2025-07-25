from decimal import Decimal
from typing import Optional

from pydantic import Field
from .base import BaseSchemaModel


class ProdSchema(BaseSchemaModel):
    name: str
    description: Optional[str] = None
    last_unit_price: Optional[Decimal] = Field(default=None, gt=0)
    curr_unit_price: Decimal = Field(..., gt=0)
    selling_price: Optional[Decimal] = Field(default=None, gt=0)
    stock_quantity: int
    category_id: Optional[int] = None


class UpdateProdSchema(BaseSchemaModel):
    name: Optional[str] = None
    description: Optional[str] = None
    last_unit_price: Optional[Decimal] = Field(default=None, gt=0)
    curr_unit_price: Optional[Decimal] = Field(default=None, gt=0)
    selling_price: Optional[Decimal] = Field(default=None, gt=0)
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None


class PartialCategorySchema(BaseSchemaModel):
    id: int
    name: str


class ProdResSchema(BaseSchemaModel):
    id: int
    name: str
    description: Optional[str]
    thumbnail: Optional[str] = None
    last_unit_price: Optional[float] = None
    curr_unit_price: float
    selling_price: Optional[float] = None
    stock_quantity: int
    category: Optional[PartialCategorySchema] = None
