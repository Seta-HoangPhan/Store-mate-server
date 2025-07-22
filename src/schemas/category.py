from typing import Optional

from .base import BaseSchemaModel
from .product import ProdResSchema


class CatSchema(BaseSchemaModel):
    name: str
    description: Optional[str] = None


class UpdateCatSchema(BaseSchemaModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CatResSchema(BaseSchemaModel):
    id: int
    name: str
    description: Optional[str] = None
    products: list[ProdResSchema] = []
