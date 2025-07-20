from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from dependencies.get_db import get_db
from dependencies.get_me import get_me
from schemas.product import ProductSchema

router = APIRouter(prefix="products", dependencies=[Depends(get_me)])


def parse_product_form(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    last_unit_price: Optional[Decimal] = Form(None),
    curr_unit_price: Decimal = Form(...),
    selling_price: Optional[Decimal] = Form(...),
    stock_quantity: int = Form(...),
    category_id: Optional[int] = Form(None),
):
    return ProductSchema(
        name=name,
        description=description,
        last_unit_price=last_unit_price,
        curr_unit_price=curr_unit_price,
        selling_price=selling_price,
        stock_quantity=stock_quantity,
        category_id=category_id,
    )


@router.post("")
def create_product(
    data: ProductSchema = Depends(parse_product_form),
    thumbnail: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return ""
