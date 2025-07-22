from fastapi import UploadFile
from sqlalchemy.orm import Session

from cloudinary_config import upload_image_to_cloudinary, delete_image
from models.product import Category, Product
from response import err_msg, exception_res, success_msg, success_res
from schemas.product import ProductResponseSchema, ProductSchema, UpdateProductSchema

RESOURCE = "Product"


# allow admin create product first time
def create_new_product(data: ProductSchema, thumnail_file: UploadFile, db: Session):
    db_product = db.query(Product).filter(Product.name == data.name).first()
    if db_product:
        return exception_res.conflict(err_msg.exist(RESOURCE))

    if data.category_id:
        db_category = db.query(Category).filter(Category.id == data.category_id).first
        if not db_category:
            return exception_res.not_found(err_msg.not_found("category"))

    upload = None
    if thumnail_file:
        upload = upload_image_to_cloudinary(thumnail_file)

    new_product = Product(
        name=data.name,
        description=data.description,
        thumbnail=upload["secure_url"] if upload else None,
        thumbnail_id=upload["public_id"] if upload else None,
        last_unit_price=data.last_unit_price,
        curr_unit_price=data.curr_unit_price,
        selling_price=data.selling_price,
        stock_quantity=data.stock_quantity,
        category_id=data.category_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return success_res.create(
        data=ProductResponseSchema.model_validate(new_product).model_dump(),
        detail=success_msg.create(RESOURCE),
    )


def update_product_by_id(
    data: UpdateProductSchema, id: int, thumnail_file: UploadFile, db: Session
):
    db_prod = db.query(Product).filter(Product.id == id).first()
    if not db_prod:
        return exception_res.conflict(err_msg.not_found(RESOURCE))

    if data.category_id:
        db_cat = db.query(Category).filter(Category.id == data.category_id).first()
        if not db_cat:
            return exception_res.conflict(err_msg.not_found("Category"))

    update_data = data.model_dump(exclude_unset=True, exclude_none=True)

    if thumnail_file:
        if db_prod.thumbnail_id:
            delete_image(db_prod.thumbnail_id)

        upload = upload_image_to_cloudinary(thumnail_file)
        update_data["thumbnail"] = upload["secure_url"] if upload else None
        update_data["thumbnail_id"] = upload["public_id"] if upload else None

    for key, value in update_data.items():
        setattr(db_prod, key, value)

    db.commit()
    db.refresh(db_prod)

    return success_res.ok(
        data=ProductResponseSchema.model_validate(db_prod).model_dump(),
        detail=success_msg.update(RESOURCE),
    )
