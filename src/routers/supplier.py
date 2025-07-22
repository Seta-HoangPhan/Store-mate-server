from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from dependencies import get_db, get_me
from schemas.supplier import SupplierSchema, UpdateSupplierSchema
from services import supplier as service

router = APIRouter(prefix="/suppliers", dependencies=[Depends(get_me)])


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return service.get_all_suppliers(db)


@router.get("/search")
def search_by_name(name: str = Query(...), db: Session = Depends(get_db)):
    return service.search_suppliers_by_name(name, db)


@router.post("")
def create_new(data: SupplierSchema, db: Session = Depends(get_db)):
    return service.create_supplier(data, db)


@router.put("/{id}")
def update_by_id(id: int, data: UpdateSupplierSchema, db: Session = Depends(get_db)):
    return service.update_supplier(data, id, db)
