from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_me
from schemas.category import CatSchema, UpdateCatSchema
from services import category as service

router = APIRouter(
    prefix="/categories", dependencies=[Depends(get_me)], redirect_slashes=True
)


@router.get("")
def get_all_cats(db: Session = Depends(get_db)):
    return service.get_all_cats(db)


@router.get("/{id}")
def get_cat_by_id(id: int, db: Session = Depends(get_db)):
    return service.get_cat_by_id(id, db)


@router.get("/{id}/products")
def get_prods_by_cat(id: int, db: Session = Depends(get_db)):
    return service.get_all_prods_by_cat(id, db)


@router.post("")
def create_new_cat(data: CatSchema, db: Session = Depends(get_db)):
    return service.create_new_cat(data, db)


@router.delete("/{id}")
def delete_cat_by_id(id: int, db: Session = Depends(get_db)):
    return service.delete_cat_by_id(db, id)


@router.put("/{id}")
def update_cat_by_id(
    id: int, data: UpdateCatSchema = Body(...), db: Session = Depends(get_db)
):
    return service.update_cat_by_id(data, db, id)
