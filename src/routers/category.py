from fastapi import APIRouter, Depends
from dependencies import get_me, get_db
from schemas.category import CategorySchema, UpdateCategorySchema
from sqlalchemy.orm import Session
from services import category as service

router = APIRouter(prefix="/categories", dependencies=[Depends(get_me)])


@router.get("")
def get_all_categories(db: Session = Depends(get_db)):
    return service.get_all_categories(db)


@router.post("")
def create_category(data: CategorySchema, db: Session = Depends(get_db)):
    return service.create_category(data, db)


@router.patch("/{id}")
def update_category(data: UpdateCategorySchema, id: int, db: Session = Depends(get_db)):
    return service.update_category_by_id(data, db, id)


@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    return service.delete_category_by_id(db, id)
