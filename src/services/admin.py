from sqlalchemy.orm import Session

from models.admin import Admin
from response import err_msg, exception_res, success_msg, success_res
from schemas.admin import AdminSchema, DeleteAdminSchema, AdminResponseSchema
from schemas.auth import VerifyOTPSchema, ResendOTPSchema
from services import auth

RESOURCE = "Admin"


def check_root_admin(me: dict, db: Session) -> bool:
    root_admin = (
        db.query(Admin).filter(Admin.phone == me["phone"], Admin.is_root).first()
    )
    if not root_admin:
        return exception_res.forbidden(err_msg.FORBIDDEN)


# only root admin can query all admins
def get_all_admins(db: Session, me: dict):
    check_root_admin(me, db)
    admins = db.query(Admin).filter(~Admin.is_root).all()
    print(f"Admins: {admins}")
    return success_res.ok(
        data=[
            AdminResponseSchema.model_validate(admin).model_dump() for admin in admins
        ]
    )


def request_admin_creation(data: AdminSchema, db: Session, me: dict):
    check_root_admin(me, db)
    return auth.create_temp_admin(data, db, is_root=False)


def resend_otp(data: ResendOTPSchema, db: Session, me: dict):
    check_root_admin(me, db)
    return auth.re_send_otp(data, db)


def verify_otp(data: VerifyOTPSchema, db: Session, me: dict):
    check_root_admin(me, db)
    return auth.verify_otp(verify=data, db=db, resource=RESOURCE)


def delete_admin(data: DeleteAdminSchema, db: Session, me: dict):
    check_root_admin(me, db)

    db_admin = db.query(Admin).filter(Admin.phone == data.phone).first()
    if not db_admin:
        return exception_res.not_found(err_msg.not_found(RESOURCE))

    if db_admin.is_root:
        return exception_res.forbidden(err_msg.CAN_NOT_DELETE_ROOT_ADMIN)

    db.delete(db_admin)
    db.commit()
    return success_res.ok(detail=success_msg.delete(RESOURCE))
