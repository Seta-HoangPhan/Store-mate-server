from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from schemas.supplier import SupResSchema

from .base import BaseSchemaModel, discount_validator
from pydantic import field_serializer


class PurProdSchema(BaseSchemaModel):
    product_id: int
    unit_price: Decimal
    discount: Optional[Decimal] = Decimal(0.00)
    quantity: int

    _validate_discount = discount_validator()


class PurSchema(BaseSchemaModel):
    supplier_id: int
    import_date: Optional[date | datetime] = None
    is_update_product: bool
    products: list[PurProdSchema]


class UpdatePurProdSchema(BaseSchemaModel):
    id: int
    product_id: Optional[int] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    quantity: Optional[int] = None

    _validate_discount = discount_validator()


class UpdatePurSchema(BaseSchemaModel):
    supplier_id: Optional[int] = None
    import_date: Optional[date] = None
    is_update_product: Optional[bool] = None
    products: Optional[list[UpdatePurProdSchema]] = None


class ProdInPurProdSchema(BaseSchemaModel):
    id: int
    name: str


class PurInPurProdSchema(BaseSchemaModel):
    id: int
    supplier: SupResSchema
    import_date: datetime

    @field_serializer("import_date", when_used="always")
    def serialize_import_date(self, value: datetime) -> str:
        return value.isoformat()


class PurProdResSchema(BaseSchemaModel):
    id: int
    product: ProdInPurProdSchema
    purchase: PurInPurProdSchema
    unit_price: float
    discount: float
    quantity: int


class PurResSchema(BaseSchemaModel):
    id: int
    supplier: SupResSchema
    purchase_products: list[PurProdResSchema]


class UpdateSupplierSchema(BaseSchemaModel):
    supplier_id: int


class CreateMultiPurProdSchema(BaseSchemaModel):
    purchase_id: int
    pur_prods: list[PurProdSchema]


class DeleteMultiPurProdSchema(BaseSchemaModel):
    ids: list[int]
