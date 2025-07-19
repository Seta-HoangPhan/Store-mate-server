from sqlalchemy.orm import Session

from response import err_msg, exception_res, success_msg, success_res


def create(db: Session, resource: str, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return success_res.create(
        data=instance,
        detail=success_msg.create(resource),
    )


def get_all(db: Session, model):
    instances = db.query(model).all()
    return success_res.ok(data=instances)


def get_by_id(db: Session, resource: str, model, id: int):
    instance = find_by_id(db, resource, model, id)
    return success_res.ok(data=instance)


def update_by_id(db: Session, resource: str, model, id: int, **kwargs):
    instance = find_by_id(db, resource, model, id)
    for key, value in kwargs.items():
        setattr(instance, key, value)
    db.commit()
    db.refresh(instance)
    return success_res.ok(
        data=instance,
        detail=success_msg.update(resource),
    )


def delete_by_id(db: Session, resource: str, model, id: int):
    instance = find_by_id(db, resource, model, id)
    db.delete(instance)
    db.commit()
    return success_res.ok(
        detail=success_msg.delete(resource),
        data={"id": instance.id},  # use `instance.id` not `instance["id"]`
    )


def find_by_id(db: Session, resource: str, model, id: int):
    instance = db.query(model).filter(model.id == id).first()
    if not instance:
        return exception_res.conflict(err_msg.not_found(resource))
    return instance
