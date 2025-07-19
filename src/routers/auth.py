from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.get_db import get_db
from schemas.admin import AdminSchema, ResendOTPSchema, VerifyOTPSchema
from services import auth

router = APIRouter(prefix="/auth")


@router.post("/register-first-admin")
async def register_first_admin(admin_info: AdminSchema, db: Session = Depends(get_db)):
    return auth.request_first_admin_otp(admin_info, db)


@router.post("/resend-otp")
async def resend_otp(resend: ResendOTPSchema, db: Session = Depends(get_db)):
    return auth.re_send_otp(resend.phone, db)


@router.post("/verify-otp")
async def verify_otp(otp_info: VerifyOTPSchema, db: Session = Depends(get_db)):
    return auth.verify_otp(otp_info, db)


@router.post("/login")
async def login(credentials: dict, db: Session = Depends(get_db)):
    # Implement your login logic here
    return {"message": "Login successful"}


@router.patch("/update-profile")
async def update_profile(user_id: int, profile_data: dict):
    # Implement your update profile logic here
    return {"message": "Profile updated successfully"}


@router.post("/forgot-password")
async def forgot_password(email: str):
    # Implement your forgot password logic here
    return {"message": "Password reset link sent"}
