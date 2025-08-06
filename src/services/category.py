from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.product import Category
from response import err_msg, exception_res, success_msg, success_res
from schemas.category import (
    CatResSchema,
    CatSchema,
    UpdateCatSchema,
)
from utils import convert_to_dict_data, convert_update_data

RESOURCE = "Category"


def find_cat_by_id(id: int, db: Session):
    db_prod = db.query(Category).filter(Category.id == id).first()
    if not db_prod:
        return exception_res.not_found(err_msg.not_found(RESOURCE))
    return db_prod


def get_all_cats(db: Session):
    db_cats = db.query(Category).order_by(desc(Category.created_at)).all()

    return success_res.ok(
        data=[convert_to_dict_data(CatResSchema, cat) for cat in db_cats]
    )


def get_cat_by_id(id: int, db: Session):
    db_cat = find_cat_by_id(id, db)

    return success_res.ok(data=convert_to_dict_data(CatResSchema, db_cat))


def get_all_prods_by_cat(cat_id: int, db: Session):
    db_cat = db.query(Category).filter(Category.id == cat_id).first()
    if not db_cat:
        return exception_res.conflict(err_msg.not_found(RESOURCE))

    dict_cat = convert_to_dict_data(CatResSchema, db_cat)

    return success_res.ok(data=dict_cat["products"])


def create_new_cat(data: CatSchema, db: Session):
    db_cat = db.query(Category).filter(Category.name == data.name).first()
    if db_cat:
        return exception_res.conflict(err_msg.exist(RESOURCE))

    new_cat = Category(name=data.name, description=data.description)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return success_res.create(
        data=convert_to_dict_data(CatResSchema, new_cat),
        detail=success_msg.create(RESOURCE),
    )


def update_cat_by_id(data: UpdateCatSchema, db: Session, id: int):
    db_cat = db.query(Category).filter(Category.id == id).first()
    if not db_cat:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    update_data = convert_update_data(data)
    for key, value in update_data.items():
        setattr(db_cat, key, value)

    db.commit()
    db.refresh(db_cat)

    return success_res.ok(
        data=convert_to_dict_data(CatResSchema, db_cat),
        detail=success_msg.update(RESOURCE),
    )


def delete_cat_by_id(db: Session, id: int):
    db_cat = db.query(Category).filter(Category.id == id).first()
    if not db_cat:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    db.delete(db_cat)
    db.commit()

    return success_res.ok(data={"id": db_cat.id}, detail=success_msg.delete(RESOURCE))
