from functools import reduce

from sqlalchemy import exists
from sqlalchemy.orm import Session

from models.purchase import Purchase, PurchaseProduct
from models.supplier import Supplier
from response import err_msg, exception_res, success_msg, success_res
from schemas.purchase import (
    CreateMultiPurProdSchema,
    DeleteMultiPurProdSchema,
    PurProdSchema,
    PurResSchema,
    PurSchema,
    UpdateSupplierSchema,
    UpdatePurSchema,
    UpdatePurProdSchema,
)
from utils import convert_decimal, convert_to_dict_data, convert_update_data

from .product import find_prod_by_id
from .supplier import find_sup_by_id
from typing import Optional

PUR_RESOURCE = "Purchase"
PUR_PROD_RESOURCE = "Purchase product"
RE_CALCULATE_FIELDS = {"unit_price", "discount", "quantity"}


def find_pur_by_id(id: int, db: Session):
    db_pur = db.query(Purchase).filter(Purchase.id == id).first()
    if not db_pur:
        return exception_res.not_found(err_msg.not_found(PUR_RESOURCE))
    return db_pur


def find_pur_prod_by_id(id: int, db: Session):
    db_pur_prod = db.query(PurchaseProduct).filter(PurchaseProduct.id == id).first()
    if not db_pur_prod:
        return exception_res.not_found(err_msg.not_found(PUR_PROD_RESOURCE))
    return db_pur_prod


def cal_total_amount(pur_prods: list[PurProdSchema]):
    return reduce(
        lambda acc, val: acc
        + val.unit_price * ((100 - val.discount) / 100) * val.quantity,
        pur_prods,
        0,
    )


def get_all_purs(db: Session):
    db_purs = db.query(Purchase).all()

    for pur in db_purs:
        pur_prods = pur.purchase_products
        print(len(pur_prods))


def create_new_pur_prod(
    data: PurProdSchema, purchase_id: int, is_update_prod: bool, db: Session
):
    db_prod = find_prod_by_id(data.product_id, db)

    unit_price = convert_decimal(data.unit_price)
    new_pur_prod = PurchaseProduct(
        purchase_id=purchase_id,
        product_id=data.product_id,
        unit_price=unit_price,
        discount=data.discount,
        quantity=data.quantity,
    )
    db.add(new_pur_prod)

    # update product quantity
    if is_update_prod:
        db_prod.quantity = db_prod.quantity + data.quantity


def create_multi_pur_prods(data: CreateMultiPurProdSchema, db: Session):
    pur_prods = data.pur_prods
    pur_id = data.purchase_id

    if len(data.pur_prods) == 0:
        return exception_res.payment_required(err_msg.missing("purchase product info"))

    db_pur = find_pur_by_id(pur_id, db)
    for pur_prod in pur_prods:
        create_new_pur_prod(pur_prod, db_pur.id, db_pur.is_update_product, db)

    db.commit()

    return success_res.create(detail=success_msg.create(PUR_PROD_RESOURCE))


def create_new_pur(data: PurSchema, db: Session):
    sup_id = data.supplier_id
    pur_prods = data.products
    is_update_prod = data.is_update_product
    import_date = data.import_date

    if not db.query(exists().where(Supplier.id == sup_id)).scalar():
        return exception_res.not_found(err_msg.not_found("Supplier"))

    new_pur = Purchase(
        supplier_id=sup_id, is_update_product=is_update_prod, import_date=import_date
    )

    db.add(new_pur)
    db.flush()

    # add purchase products
    for pp in pur_prods:
        create_new_pur_prod(pp, new_pur.id, is_update_prod, db)

    db.commit()
    db.refresh(new_pur)

    return success_res.create(
        data=convert_to_dict_data(PurResSchema, new_pur),
        detail=success_msg.create(PUR_RESOURCE),
    )


def update_pur_prod(
    data: UpdatePurProdSchema, is_update_prod: Optional[bool], db: Session
):
    db_pur_prod = find_pur_prod_by_id(data.id, db)
    pur_prod_quantity = db_pur_prod.quantity
    update_data = convert_update_data(data)
    for key, val in update_data.items():
        setattr(db_pur_prod, key, val)

    # is_update_prod=True, update add product quantity
    # is_update_prod=False, update product quantity back to the initial val
    # is_update_prod=None, doesn't update product
    db_prod = find_prod_by_id(data.product_id, db)
    if is_update_prod is True:
        db_prod.quantity = db_prod.quantity + data.quantity
    elif is_update_prod is False:
        db_prod.quantity = db_prod.quantity - pur_prod_quantity


def update_pur_by_id(data: UpdatePurSchema, id: int, db: Session):
    sup_id = data.supplier_id
    import_date = data.import_date
    is_update_prod = data.is_update_product
    prods = data.products

    db_pur = find_pur_by_id(id, db)
    if sup_id:
        db_pur.supplier_id = sup_id
    if import_date:
        db_pur.import_date = import_date
    if is_update_prod:
        if db_pur.is_update_product == is_update_prod:
            is_update_prod = None
        else:
            db_pur.is_update_product = is_update_prod
    if prods:
        for prod in prods:
            update_pur_prod(prod, is_update_prod, db)

    db.commit()
    db.refresh(db_pur)

    return success_res.ok(data=convert_to_dict_data(PurResSchema, db_pur))


def update_supplier_id(data: UpdateSupplierSchema, purchase_id: int, db: Session):
    if not purchase_id:
        return exception_res.payment_required(err_msg.missing("purchase id"))

    db_sup = find_sup_by_id(data.supplier_id, db)
    db_pur = find_pur_by_id(purchase_id, db)
    setattr(db_pur, "supplier_id", db_sup.id)

    db.commit()
    db.refresh(db_pur)

    return success_res.ok(
        data=convert_to_dict_data(PurResSchema, db_pur),
        detail=success_msg.update(PUR_RESOURCE),
    )


def delete_pur_prod_by_ids(data: DeleteMultiPurProdSchema, db: Session):
    if len(data.ids) == 0:
        return exception_res.payment_required(err_msg.missing("purchase product ids"))

    for id in data.ids:
        db_pur_prod = find_pur_prod_by_id(id, db)
        db.delete(db_pur_prod)

    db.commit()

    return success_res.ok(detail=success_msg.delete(PUR_PROD_RESOURCE))
