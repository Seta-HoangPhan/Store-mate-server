from sqlalchemy import exists, func
from sqlalchemy.orm import Session

from models.supplier import Supplier, SupplierPhone
from response import err_msg, exception_res, success_msg, success_res
from schemas.supplier import SupResSchema, SupSchema, UpdateSupSchema
from utils import convert_to_dict_data, convert_update_data

RESOURCE = "Supplier"


def get_all_sups(db: Session):
    db_suppliers = db.query(Supplier).all()
    return success_res.ok(
        data=[convert_to_dict_data(SupResSchema, supplier) for supplier in db_suppliers]
    )


def search_sups_by_name(search: str, db: Session):
    db_suppliers = (
        db.query(Supplier)
        .filter(func.unaccent(Supplier.name).ilike(f"%{search}%"))
        .all()
    )
    return success_res.ok(
        data=[convert_to_dict_data(SupResSchema, supplier) for supplier in db_suppliers]
    )


def create_new_sup(data: SupSchema, db: Session):
    name = data.name.strip()
    phones = data.phones
    email = data.email.strip().lower() if data.email else None
    address = data.address.strip() if data.address else None

    if db.query(exists().where(func.lower(Supplier.name) == name.lower())).scalar():
        return exception_res.conflict(err_msg.exist("Supplier name"))

    if db.query(exists().where(SupplierPhone.phone.in_(phones))).scalar():
        return exception_res.conflict(err_msg.exist("Supplier phone"))

    if data.email:
        if db.query(exists().where(Supplier.email == email)).scalar():
            return exception_res.conflict(err_msg.exist("Supplier email"))

    new_sup = Supplier(
        name=name,
        email=email,
        address=address,
    )

    db.add(new_sup)
    db.flush()

    for phone in phones:
        new_sup_phone = SupplierPhone(phone=phone.strip(), supplier_id=new_sup.id)
        db.add(new_sup_phone)

    db.commit()
    db.refresh(new_sup)

    return success_res.create(
        data=convert_to_dict_data(SupResSchema, new_sup),
        detail=success_msg.create(RESOURCE),
    )


def update_sup_phone(data: dict, sup_id: int, db: Session):
    db_sup_phone = (
        db.query(SupplierPhone)
        .filter(SupplierPhone.id == data["id"], SupplierPhone.supplier_id == sup_id)
        .first()
    )
    if not db_sup_phone:
        return exception_res.not_found(err_msg.not_found("Supplier phone"))

    setattr(db_sup_phone, "phone", data["phone"])


def update_sup(data: UpdateSupSchema, id: int, db: Session):
    db_sup = db.query(Supplier).filter(Supplier.id == id).first()
    if not db_sup:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    update_data = convert_update_data(data)
    for key, value in update_data.items():
        if key != "phones":
            setattr(db_sup, key, value)

    if len(update_data["phones"]) > 0:
        for phone in update_data["phones"]:
            update_sup_phone(phone, db_sup.id, db)

    db.commit()
    db.refresh(db_sup)

    return success_res.create(
        data=convert_to_dict_data(SupResSchema, db_sup),
        detail=success_msg.update(RESOURCE),
    )
