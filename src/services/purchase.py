from sqlalchemy import exists
from sqlalchemy.orm import Session

from models.product import Product
from models.purchase import Purchase, PurchaseProduct
from models.supplier import Supplier
from response import err_msg, exception_res, success_msg, success_res
from schemas.purchase import (
    PurchaseProductSchema,
    PurchaseResponseSchema,
    PurchaseSchema,
    UpdatePurchaseProductSchema,
    UpdatePurchaseSchema,
)
from utils import convert_decimal, convert_to_dict_data, convert_update_data

RESOURCE = "Purchase"
PURCHASE_FIELDS = {"supplier_id", "total_amount"}


def create_new_purchase_product(
    data: PurchaseProductSchema, purchase_id: int, db: Session
):
    if not db.query(exists().where(Product.id == data.product_id)).scalar():
        return exception_res.not_found(err_msg.not_found("Product"))

    new_purchase_product = PurchaseProduct(
        purchase_id=purchase_id,
        product_id=data.product_id,
        unit_price=convert_decimal(data.unit_price),
        discount=data.discount,
        purchase_quantity=data.purchase_quantity,
    )
    db.add(new_purchase_product)


def create_new_purchase(data: PurchaseSchema, db: Session):
    if not db.query(exists().where(Supplier.id == data.supplier_id)).scalar():
        return exception_res.not_found(err_msg.not_found("Supplier"))

    new_purchase = Purchase(
        supplier_id=data.supplier_id, total_amount=data.total_amount
    )

    db.add(new_purchase)
    db.flush()

    for pp in data.purchase_products:
        create_new_purchase_product(pp, new_purchase.id, db)

    db.commit()
    db.refresh(new_purchase)

    return success_res.create(
        data=convert_to_dict_data(PurchaseResponseSchema, new_purchase),
        detail=success_msg.create(RESOURCE),
    )


def update_purchase_product(data: UpdatePurchaseProductSchema, db: Session):
    if not data.id:
        return exception_res.payment_required(err_msg.missing("purchase product id"))

    if data.product_id:
        if not db.query(exists().where(Product.id == data.product_id)).scalar():
            return exception_res.not_found(err_msg.not_found("Product"))

    db_purchase_prod = (
        db.query(PurchaseProduct).filter(PurchaseProduct.id == data.id).first()
    )
    if not db_purchase_prod:
        return exception_res.not_found(err_msg.not_found("Purchase product"))

    update_data = convert_update_data(data)
    for key, value in update_data.items():
        setattr(db_purchase_prod, key, value)


def update_purchase(data: UpdatePurchaseSchema, purchase_id: int, db: Session):
    if not purchase_id:
        return exception_res.payment_required(err_msg.missing("purchase id"))

    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_purchase:
        return exception_res.not_found(RESOURCE)

    update_data = convert_update_data(data)
    for key, value in update_data.items():
        if key in PURCHASE_FIELDS:
            setattr(db_purchase, key, value)

    purchase_products = update_data["purchase_products"]
    if purchase_products is not None and len(purchase_products) > 0:
        for pprod in purchase_products:
            update_purchase_product(pprod, db)

    db.commit()
    db.refresh(db_purchase)

    return success_res.ok(
        data=convert_to_dict_data(PurchaseResponseSchema, db_purchase),
        detail=success_msg.update(RESOURCE),
    )
