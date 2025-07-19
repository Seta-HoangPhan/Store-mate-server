import random
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.admin import Admin
from models.temp_admin import TempAdmin
from response import err_msg, exception_res, success_res
from schemas.admin import AdminResponseSchema, AdminSchema, VerifyOTPSchema
from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
expiration_limit = datetime.now(timezone.utc) - timedelta(
    minutes=settings.auto_delete_expired_otp_time
)


def generate_otp() -> str:
    return "".join(random.choices("0123456789", k=6))


def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


# if phone is already in TempAdmin table, delete it and create a new one
def request_first_admin_otp(admin_info: AdminSchema, db: Session):
    db_admins = db.query(Admin).filter(Admin.phone == admin_info.phone).all()
    if db_admins.__len__() > 0:
        return exception_res.conflict(err_msg.EXIST_FIRST_ADMIN)

    db_temp_admin = (
        db.query(TempAdmin).filter(TempAdmin.phone == admin_info.phone).first()
    )
    if db_temp_admin:
        db.delete(db_temp_admin)
        db.commit()

    otp = generate_otp()
    default_pwd = hash_password(settings.default_password)
    new_temp_admin = TempAdmin(
        phone=admin_info.phone,
        email=admin_info.email,
        password=default_pwd,
        otp=otp,
    )
    db.add(new_temp_admin)
    db.commit()
    db.refresh(new_temp_admin)

    # send OTP to the phone number
    # just mocking the sending process
    print(f"OTP for first admin: {otp}")

    return success_res.ok()


def re_send_otp(phone: str, db: Session):
    db_temp_admin = db.query(TempAdmin).filter(TempAdmin.phone == phone).first()
    if not db_temp_admin:
        return exception_res.conflict(err_msg.NO_OTP_REQUEST)

    otp = generate_otp()
    db_temp_admin.otp = otp
    db.commit()
    db.refresh(db_temp_admin)

    # send OTP to the phone number
    # just mocking the sending process
    print(f"OTP for re-send: {otp}")

    return success_res.ok()


def is_expired_otp(created_at: datetime, expiration: int) -> bool:
    return datetime.now(timezone.utc) - created_at > timedelta(minutes=expiration)


#  delete expired OTPs ( that > 10 mins ) from TempAdmin table every time verify_otp is called
def delete_expired_otp(db: Session):
    expired_temp_admins = (
        db.query(TempAdmin).filter(TempAdmin.created_at <= expiration_limit).all()
    )

    for temp_admin in expired_temp_admins:
        db.delete(temp_admin)

    db.commit()


# db_temp_admin: expired more than 10 mins => otp is not existed
#                expired less than 10 mins => otp is expired
def verify_otp(verify: VerifyOTPSchema, db: Session):
    # only check if the OTP is valid and expiration time < 10 mins
    db_temp_admin = (
        db.query(TempAdmin)
        .filter(
            TempAdmin.phone == verify.phone, TempAdmin.created_at > expiration_limit
        )
        .first()
    )

    # auto delete expired OTPs ( that > 10 mins )
    delete_expired_otp(db)

    if not db_temp_admin:
        return exception_res.conflict(err_msg.NO_OTP_REQUEST)

    phone, email, password, otp, created_at, expiration = (
        db_temp_admin.phone,
        db_temp_admin.email,
        db_temp_admin.password,
        db_temp_admin.otp,
        db_temp_admin.created_at,
        db_temp_admin.expiration,
    )

    if is_expired_otp(created_at, expiration):
        db.delete(db_temp_admin)
        db.commit()
        return exception_res.bad_request(err_msg.EXPIRED_OTP)

    if otp != verify.otp:
        return exception_res.bad_request(err_msg.INVALID_OTP)

    new_admin = Admin(
        phone=phone,
        email=email,
        password=password,
    )
    db.add(new_admin)
    db.delete(db_temp_admin)
    db.commit()
    db.refresh(new_admin)

    return success_res.ok(
        data=AdminResponseSchema.model_validate(new_admin).model_dump(),
    )
