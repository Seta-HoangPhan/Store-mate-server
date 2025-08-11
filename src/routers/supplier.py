from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from dependencies import get_db, get_me
from schemas.supplier import SupSchema, UpdateSupSchema
from services import supplier as service

router = APIRouter(prefix="/suppliers", dependencies=[Depends(get_me)])


@router.get("")
def get_all_sups(db: Session = Depends(get_db)):
    return service.get_all_sups(db)


@router.get("/{id}")
def get_sup_by_id(id: int, db: Session = Depends(get_db)):
    return service.get_sup_by_id(id, db)


@router.get("/search")
def search_sups_by_name(name: str = Query(...), db: Session = Depends(get_db)):
    return service.search_sups_by_name(name, db)


@router.post("")
def create_new_sup(data: SupSchema, db: Session = Depends(get_db)):
    return service.create_new_sup(data, db)


@router.put("/{id}")
def update_sup(id: int, data: UpdateSupSchema, db: Session = Depends(get_db)):
    return service.update_sup(data, id, db)
