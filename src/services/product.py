from fastapi import UploadFile
from sqlalchemy import exists
from sqlalchemy.orm import Session

from cloudinary_config import delete_image, upload_image_to_cloudinary
from models.product import Category, Product
from response import err_msg, exception_res, success_msg, success_res
from schemas.product import ProdResSchema, ProdSchema, UpdateProdSchema
from utils import convert_decimal, convert_to_dict_data, convert_update_data

RESOURCE = "Product"
DECIMAL_FIELDS = {"last_unit_price", "curr_unit_price", "selling_price"}


def find_prod_by_id(id: int, db: Session):
    db_prod = db.query(Product).filter(Product.id == id).first()
    if not db_prod:
        return exception_res.not_found(err_msg.not_found(RESOURCE))
    return db_prod


# allow admin create product first time
def create_new_prod(data: ProdSchema, thumnail_file: UploadFile, db: Session):
    if db.query(exists().where(Product.name == data.name)).scalar():
        return exception_res.conflict(err_msg.exist(RESOURCE))

    if data.category_id:
        if not db.query(exists().where(Category.id == data.category_id)).scalar():
            return exception_res.not_found(err_msg.not_found("category"))

    upload = None
    if thumnail_file:
        upload = upload_image_to_cloudinary(thumnail_file)

    new_product = Product(
        name=data.name,
        description=data.description,
        thumbnail=upload["secure_url"] if upload else None,
        thumbnail_id=upload["public_id"] if upload else None,
        last_unit_price=convert_decimal(data.last_unit_price),
        curr_unit_price=convert_decimal(data.curr_unit_price),
        selling_price=convert_decimal(data.selling_price),
        stock_quantity=data.stock_quantity,
        category_id=data.category_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return success_res.create(
        data=convert_to_dict_data(ProdResSchema, new_product),
        detail=success_msg.create(RESOURCE),
    )


def update_prod_by_id(
    data: UpdateProdSchema, id: int, thumnail_file: UploadFile, db: Session
):
    db_prod = find_prod_by_id(id, db)

    if data.category_id:
        if not db.query(exists().where(Category.id == data.category_id)).scalar():
            return exception_res.conflict(err_msg.not_found("Category"))

    update_data = convert_update_data(data)

    if thumnail_file:
        if db_prod.thumbnail_id:
            delete_image(db_prod.thumbnail_id)

        upload = upload_image_to_cloudinary(thumnail_file)
        update_data["thumbnail"] = upload["secure_url"] if upload else None
        update_data["thumbnail_id"] = upload["public_id"] if upload else None

    for key, value in update_data.items():
        if key in DECIMAL_FIELDS:
            update_data[key] = convert_decimal(value)

        setattr(db_prod, key, value)

    db.commit()
    db.refresh(db_prod)

    return success_res.ok(
        data=convert_to_dict_data(ProdResSchema, db_prod),
        detail=success_msg.update(RESOURCE),
    )
