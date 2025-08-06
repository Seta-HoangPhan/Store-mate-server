from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_me
from schemas.admin import AdminSchema
from schemas.auth import (
    LoginSchema,
    ResendOTPSchema,
    VerifyOTPSchema,
    RefreshTokenSchema,
)
from services import auth as service

router = APIRouter(prefix="/auth")


@router.post("/register-first-admin")
def register_first_admin(admin_info: AdminSchema, db: Session = Depends(get_db)):
    return service.request_root_admin_creation(admin_info, db)


@router.post("/resend-otp")
def resend_otp(resend: ResendOTPSchema, db: Session = Depends(get_db)):
    return service.resend_otp(resend, db)


@router.post("/verify-otp")
def verify_otp(otp_info: VerifyOTPSchema, db: Session = Depends(get_db)):
    return service.verify_otp(otp_info, db)


@router.get("/get-profile")
def get_profile(user=Depends(get_me)):
    return service.get_profile(user)


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return service.login(data, db)


@router.post("/refresh-token")
def regenerate_access_token(data: RefreshTokenSchema, db: Session = Depends(get_db)):
    return service.regenerate_access_token(data, db)


# @router.patch("/update-profile")
# def update_profile(user_id: int, profile_data: dict, me: dict = Depends(get_curr_user)):
#     # Implement your update profile logic here
#     return {"message": "Profile updated successfully"}


# @router.post("/forgot-password")
# def forgot_password(email: str):
#     # Implement your forgot password logic here
#     return {"message": "Password reset link sent"}
