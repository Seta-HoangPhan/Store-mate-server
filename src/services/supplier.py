from sqlalchemy import exists, func, desc
from sqlalchemy.orm import Session

from models.supplier import Supplier, SupplierPhone
from response import err_msg, exception_res, success_msg, success_res
from schemas.supplier import SupResSchema, SupSchema, UpdateSupSchema, UpdatePhoneSchema
from utils import convert_to_dict_data, convert_update_data

RESOURCE = "Supplier"


def get_data(data: Supplier | list[Supplier]):
    if isinstance(data, list):
        return [convert_to_dict_data(SupResSchema, supplier) for supplier in data]

    return convert_to_dict_data(SupResSchema, data)


def find_sup_by_id(id: int, db: Session):
    db_sup = db.query(Supplier).filter(Supplier.id == id).first()
    if not db_sup:
        return exception_res.not_found(err_msg.not_found(RESOURCE))
    return db_sup


def get_all_sups(db: Session):
    db_suppliers = db.query(Supplier).order_by(desc(Supplier.created_at)).all()
    return success_res.ok(data=get_data(db_suppliers))


def get_sup_by_id(id: int, db: Session):
    db_sup = find_sup_by_id(id, db)
    return success_res.ok(data=get_data(db_sup))


def search_sups_by_name(search: str, db: Session):
    db_suppliers = (
        db.query(Supplier)
        .filter(func.unaccent(Supplier.name).ilike(f"%{search}%"))
        .all()
    )
    return success_res.ok(data=get_data(db_suppliers))


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
        data=get_data(new_sup),
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
    db_sup = find_sup_by_id(id, db)

    phones = [
        UpdatePhoneSchema(**p) if isinstance(p, dict) else p
        for p in (data.phones or [])
    ]
    phones_ids = [phone.id for phone in phones if phone.id is not None]

    update_data = convert_update_data(data)
    for key, value in update_data.items():
        if key != "phones":
            setattr(db_sup, key, value)

    # delete all phones nin db that don't exist in request phones list
    db.query(SupplierPhone).filter(
        SupplierPhone.supplier_id == id, ~SupplierPhone.id.in_(phones_ids)
    ).delete(synchronize_session=False)

    for phone in phones:
        if phone.id is None:
            new_sup_phone = SupplierPhone(phone=phone.phone.strip(), supplier_id=id)
            db.add(new_sup_phone)
        else:
            update_sup_phone(phone, db_sup.id, db)

    db.commit()
    db.refresh(db_sup)

    return success_res.ok(
        data=get_data(db_sup),
        detail=success_msg.update(RESOURCE),
    )
