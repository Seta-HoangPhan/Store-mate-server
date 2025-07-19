from fastapi import APIRouter

router = APIRouter()


@router.post("/create-admin")
async def create_admin(admin_data: dict):
    # Implement your create admin logic here
    return {"message": "Admin created successfully"}
