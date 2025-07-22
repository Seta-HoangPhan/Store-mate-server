from decimal import Decimal
from typing import Optional

from schemas.supplier import SupResSchema

from .base import BaseSchemaModel, discount_validator


class PurchaseProductSchema(BaseSchemaModel):
    product_id: int
    unit_price: Decimal
    discount: Optional[Decimal] = None
    purchase_quantity: int

    _validate_discount = discount_validator()


class PurchaseSchema(BaseSchemaModel):
    supplier_id: int
    total_amount: Decimal
    purchase_products: list[PurchaseProductSchema]


class PurchaseProductResponseSchema(BaseSchemaModel):
    id: int
    unit_price: float
    discount: Optional[float] = None
    purchase_quantity: int


class PurchaseResponseSchema(BaseSchemaModel):
    id: int
    supplier: SupResSchema
    total_amount: float
    purchase_products: list[PurchaseProductResponseSchema]


class UpdatePurchaseProductSchema(BaseSchemaModel):
    id: int
    product_id: Optional[int] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    purchase_quantity: Optional[int] = None

    _validate_discount = discount_validator()


class UpdatePurchaseSchema(BaseSchemaModel):
    supplier_id: Optional[int] = None
    total_amount: Optional[Decimal] = None
    purchase_products: Optional[list[UpdatePurchaseProductSchema]] = None
