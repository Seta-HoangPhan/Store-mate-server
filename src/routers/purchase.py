from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_me
from schemas.purchase import PurSchema, UpdatePurSchema
from services import purchase as service

router = APIRouter(prefix="/purchases", dependencies=[Depends(get_me)])


@router.post("")
def create_new_pur(data: PurSchema, db: Session = Depends(get_db)):
    return service.create_new_pur(data, db)


@router.put("/{id}")
def update_pur_by_id(data: UpdatePurSchema, id: int, db: Session = Depends(get_db)):
    return service.update_pur_by_id(data, id, db)
