from decimal import Decimal
from typing import Optional

from schemas.supplier import SupplierResponseSchema

from .base import BaseSchemaModel, discount_validator


class PurchaseProductSchema(BaseSchemaModel):
    purchase_id: int
    product_id: int
    unit_price: Decimal
    discount: Optional[Decimal] = None
    purchase_quantity: int

    _validate_discount = discount_validator()


class PurchaseProductResponseSchema(BaseSchemaModel):
    id: int
    unit_price: float
    discount: Optional[float] = None
    purchase_quantity: int


class PurchaseSchema(BaseSchemaModel):
    supplier_id: int
    total_amount: Decimal


class PurchaseResponseSchema(BaseSchemaModel):
    id: int
    supplier: SupplierResponseSchema
    total_amount: float
    purchase_products: list[PurchaseProductResponseSchema]
