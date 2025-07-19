import random
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.admin import Admin
from models.temp_admin import TempAdmin
from response import err_msg, exception_res, success_msg, success_res
from schemas.admin import AdminResponseSchema, AdminSchema
from schemas.auth import (
    LoginSchema,
    RefreshTokenSchema,
    VerifyOTPSchema,
    ResendOTPSchema,
)
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


def create_temp_admin(data: AdminSchema, db: Session, is_root: bool = False):
    db_temp_admin = db.query(TempAdmin).filter(TempAdmin.phone == data.phone).first()
    if db_temp_admin:
        db.delete(db_temp_admin)
        db.commit()

    otp = generate_otp()
    default_pwd = hash_password(settings.default_password)
    new_temp_admin = TempAdmin(
        phone=data.phone,
        email=data.email,
        password=default_pwd,
        is_root=is_root,
        otp=otp,
    )
    db.add(new_temp_admin)
    db.commit()

    # send OTP to the phone number
    # just mocking the sending process
    print(f"OTP for {'root' if is_root else ''} admin: {otp}")

    return success_res.ok()


# if phone is already in TempAdmin table, delete it and create a new one
def request_root_admin_creation(admin_info: AdminSchema, db: Session):
    db_admins = db.query(Admin).filter(Admin.phone == admin_info.phone).all()
    if db_admins.__len__() > 0:
        return exception_res.conflict(err_msg.EXIST_FIRST_ADMIN)
    return create_temp_admin(admin_info, db, is_root=True)


def resend_otp(data: ResendOTPSchema, db: Session):
    db_temp_admin = db.query(TempAdmin).filter(TempAdmin.phone == data.phone).first()
    if not db_temp_admin:
        return exception_res.conflict(err_msg.NO_OTP_REQUEST)

    otp = generate_otp()
    db_temp_admin.otp = otp
    db.commit()

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
def verify_otp(verify: VerifyOTPSchema, db: Session, resource: str = "Root admin"):
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

    phone, email, password, is_root, otp, created_at, expiration = (
        db_temp_admin.phone,
        db_temp_admin.email,
        db_temp_admin.password,
        db_temp_admin.is_root,
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
        is_root=is_root,
    )
    db.add(new_admin)
    db.delete(db_temp_admin)
    db.commit()
    db.refresh(new_admin)

    return success_res.ok(
        data=AdminResponseSchema.model_validate(new_admin).model_dump(),
        detail=success_msg.create(resource),
    )


def gen_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.access_token_key, algorithm=settings.algorithm
    )


def gen_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        hours=settings.refresh_token_expire_hours
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.refresh_token_key, algorithm=settings.algorithm
    )


def login(data: LoginSchema, db: Session):
    db_admin = db.query(Admin).filter(Admin.phone == data.phone).first()
    if not db_admin:
        return exception_res.not_found(err_msg.not_found("Admin"))

    if not verify_password(data.password, db_admin.password):
        return exception_res.unauthorized(err_msg.INVALID_PASSWORD)

    data = {"id": db_admin.id, "phone": db_admin.phone, "email": db_admin.email}
    access_token = gen_access_token(data)
    refresh_token = gen_refresh_token(data)
    return success_res.ok(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "admin": AdminResponseSchema.model_validate(db_admin).model_dump(),
        }
    )


def regenerate_access_token(data: RefreshTokenSchema, db: Session):
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.refresh_token_key,
            algorithms=[settings.algorithm],
        )
    except JWTError:
        return exception_res.unauthorized(err_msg.INVALID_TOKEN)

    db_admin = db.query(Admin).filter(Admin.phone == payload["phone"]).first()
    if not db_admin:
        return exception_res.unauthorized(err_msg.NOT_FOUND_USER_OR_INVALID_TOKEN)

    access_token = gen_access_token(
        {"id": db_admin.id, "phone": db_admin.phone, "email": db_admin.email}
    )
    return success_res.ok(data={"access_token": access_token})
