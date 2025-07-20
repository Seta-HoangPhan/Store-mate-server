from typing import Optional

from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: str
    description: Optional[str] = None

    class config:
        from_attributes = True


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class config:
        from_attributes = True


class CategoryResponseSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    class config:
        from_attributes = True
