from typing import Optional

from .base import BaseSchemaModel
from .product import ProductResponseSchema


class CategorySchema(BaseSchemaModel):
    name: str
    description: Optional[str] = None


class UpdateCategorySchema(BaseSchemaModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponseSchema(BaseSchemaModel):
    id: int
    name: str
    description: Optional[str] = None
    products: list[ProductResponseSchema] = []
