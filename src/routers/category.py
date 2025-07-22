from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_me
from schemas.category import CategorySchema, UpdateCategorySchema
from services import category as service

router = APIRouter(
    prefix="/categories", dependencies=[Depends(get_me)], redirect_slashes=True
)


@router.get("")
def get_all_categories(db: Session = Depends(get_db)):
    return service.get_all_categories(db)


@router.get("/{id}/products")
def get_products_by_category(id: int, db: Session = Depends(get_db)):
    return service.get_all_products_by_category(id, db)


@router.post("")
def create_category(data: CategorySchema, db: Session = Depends(get_db)):
    return service.create_category(data, db)


@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    return service.delete_category_by_id(db, id)


@router.put("/{id}")
def update_category(
    id: int, data: UpdateCategorySchema = Body(...), db: Session = Depends(get_db)
):
    return service.update_category_by_id(data, db, id)
