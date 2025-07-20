from sqlalchemy.orm import Session
from schemas.category import (
    CategorySchema,
    CategoryResponseSchema,
    UpdateCategorySchema,
)
from models.product import Category
from response import err_msg, exception_res, success_msg, success_res

RESOURCE = "Category"


def get_all_categories(db: Session):
    db_cats = db.query(Category).all()

    return success_res.ok(
        data=[
            CategoryResponseSchema.model_validate(cat).model_dump() for cat in db_cats
        ]
    )


def create_category(data: CategorySchema, db: Session):
    db_cat = db.query(Category).filter(Category.name == data.name).first()
    if db_cat:
        return exception_res.conflict(err_msg.exist(RESOURCE))

    new_cat = Category(name=data.name, description=data.description)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return success_res.create(
        data=CategoryResponseSchema.model_validate(new_cat).model_dump(),
        detail=success_msg.create(RESOURCE),
    )


def update_category_by_id(data: UpdateCategorySchema, db: Session, id: int):
    db_cat = db.query(Category).filter(Category.id == id).first()
    if not db_cat:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_cat, key, value)

    db.commit()
    db.refresh(db_cat)

    return success_res.ok(
        data=CategoryResponseSchema.model_validate(db_cat).model_dump(),
        detail=success_msg.update(RESOURCE),
    )


def delete_category_by_id(db: Session, id: int):
    db_cat = db.query(Category).filter(Category.id == id).first()
    if not db_cat:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    db.delete(db_cat)
    db.commit()

    return success_res.ok(data={"id": db_cat.id}, detail=success_msg.delete(RESOURCE))
