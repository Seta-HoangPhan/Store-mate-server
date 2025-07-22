from typing import Optional

from pydantic import BaseModel
from .product import ProductResponseSchema


class CategorySchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    products: list[ProductResponseSchema] = []

    class Config:
        from_attributes = True
