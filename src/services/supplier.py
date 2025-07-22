from sqlalchemy import exists, func
from sqlalchemy.orm import Session

from models.supplier import Supplier
from response import err_msg, exception_res, success_msg, success_res
from schemas.supplier import (
    SupplierResponseSchema,
    SupplierSchema,
    UpdateSupplierSchema,
)

RESOURCE = "Supplier"


def get_all_suppliers(db: Session):
    db_suppliers = db.query(Supplier).all()
    return success_res.ok(
        data=[
            SupplierResponseSchema.model_validate(supplier).model_dump()
            for supplier in db_suppliers
        ]
    )


def search_suppliers_by_name(search: str, db: Session):
    db_suppliers = (
        db.query(Supplier)
        .filter(func.unaccent(Supplier.name).ilike(f"%{search}%"))
        .all()
    )
    return success_res.ok(
        data=[
            SupplierResponseSchema.model_validate(supplier).model_dump()
            for supplier in db_suppliers
        ]
    )


def create_supplier(data: SupplierSchema, db: Session):
    name = data.name.strip()
    phone = data.phone.strip()
    email = data.email.strip().lower() if data.email else None
    address = data.address.strip() if data.address else None

    if db.query(exists().where(func.lower(Supplier.name) == name.lower())).scalar():
        return exception_res.conflict(err_msg.exist("Supplier name"))

    if db.query(exists().where(Supplier.phone == phone)).scalar():
        return exception_res.conflict(err_msg.exist("Supplier phone"))

    if data.email:
        if db.query(exists().where(Supplier.email == email)).scalar():
            return exception_res.conflict(err_msg.exist("Supplier email"))

    new_supplier = Supplier(
        name=name,
        phone=phone,
        email=email,
        address=address,
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return success_res.create(
        data=SupplierResponseSchema.model_validate(new_supplier).model_dump(),
        detail=success_msg.create(RESOURCE),
    )


def update_supplier(data: UpdateSupplierSchema, id: int, db: Session):
    db_supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not db_supplier:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)

    db.commit()
    db.refresh(db_supplier)

    return success_res.create(
        data=SupplierResponseSchema.model_validate(db_supplier).model_dump(),
        detail=success_msg.update(RESOURCE),
    )
