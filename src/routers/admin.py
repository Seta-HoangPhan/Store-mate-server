from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.get_db import get_db
from dependencies.get_me import get_me
from schemas.admin import AdminSchema, DeleteAdminSchema
from schemas.auth import VerifyOTPSchema, ResendOTPSchema
from services import admin

router = APIRouter(prefix="/admins", dependencies=[Depends(get_me)])


@router.get("")
async def get_all_admins(db: Session = Depends(get_db), me: dict = Depends(get_me)):
    return admin.get_all_admins(db, me)


@router.post("/create-admin")
async def create_admin(
    admin_data: AdminSchema, db: Session = Depends(get_db), me: dict = Depends(get_me)
):
    return admin.request_admin_creation(admin_data, db, me)


@router.post("/resend-otp")
async def resend_admin_otp(otp_data: ResendOTPSchema, db: Session = Depends(get_db)):
    return admin.resend_otp(otp_data, db)


@router.post("/verify-otp")
async def verify_admin_otp(
    otp_data: VerifyOTPSchema, db: Session = Depends(get_db), me: dict = Depends(get_me)
):
    return admin.verify_otp(otp_data, db, me)


@router.delete("/delete-admin")
async def delete_admin(
    delete_data: DeleteAdminSchema,
    db: Session = Depends(get_db),
    me: dict = Depends(get_me),
):
    return admin.delete_admin(delete_data, db, me)
