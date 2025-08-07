from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, Query
from sqlalchemy.orm import Session

from dependencies.get_db import get_db
from dependencies.get_me import get_me
from schemas.product import ProdSchema, UpdateProdSchema
from services import product as service

router = APIRouter(prefix="/products", dependencies=[Depends(get_me)])


@router.get("")
def get_prods_by_cat_ids(
    cat_ids: list[int] = Query(default=[]),
    db: Session = Depends(get_db),
):
    return service.get_prods_by_cat_ids(cat_ids, db)


@router.get("/{id}")
def get_prod_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    return service.get_prod_by_id(id, db)


def parse_prod_form(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    selling_price: Optional[Decimal] = Form(...),
    quantity: int = Form(...),
    category_id: Optional[int] = Form(None),
):
    return ProdSchema(
        name=name,
        description=description,
        selling_price=selling_price,
        quantity=quantity,
        category_id=category_id,
    )


@router.post("")
def create_new_prod(
    data: ProdSchema = Depends(parse_prod_form),
    thumbnail: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    return service.create_new_prod(data, thumbnail, db)


def parse_update_product_form(
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    selling_price: Optional[Decimal] = Form(None),
    quantity: Optional[int] = Form(None),
    category_id: Optional[int] = Form(None),
):
    return UpdateProdSchema(
        name=name,
        description=description,
        selling_price=selling_price,
        quantity=quantity,
        category_id=category_id,
    )


@router.put("/{id}")
def update_prod_by_id(
    id: int,
    data: UpdateProdSchema = Depends(parse_update_product_form),
    thumbnail: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    return service.update_prod_by_id(data, id, thumbnail, db)
