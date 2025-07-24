from decimal import Decimal
from typing import Optional

from schemas.supplier import SupResSchema

from .base import BaseSchemaModel, discount_validator


class PurProdSchema(BaseSchemaModel):
    product_id: int
    unit_price: Decimal
    discount: Optional[Decimal] = Decimal(0.00)
    quantity: int

    _validate_discount = discount_validator()


class PurSchema(BaseSchemaModel):
    supplier_id: int
    products: list[PurProdSchema]
    is_update_prod: bool


class PurchaseProductResponseSchema(BaseSchemaModel):
    id: int
    unit_price: float
    discount: Optional[float] = None
    quantity: int


class PurResSchema(BaseSchemaModel):
    id: int
    supplier: SupResSchema
    purchase_products: list[PurchaseProductResponseSchema]


class UpdateSupplierSchema(BaseSchemaModel):
    supplier_id: int


class CreateMultiPurProdSchema(BaseSchemaModel):
    purchase_id: int
    pur_prods: list[PurProdSchema]


class DeleteMultiPurProdSchema(BaseSchemaModel):
    ids: list[int]
