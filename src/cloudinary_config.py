import cloudinary
import cloudinary.uploader
from settings import settings
from fastapi import UploadFile

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
    secure=True,
)


def upload_image_to_cloudinary(file: UploadFile):
    result = cloudinary.uploader.upload(file.file, folder="product_thumbnails")
    return {
        "public_id": result.get("public_id"),
        "secure_url": result.get("secure_url"),
    }


def delete_image_from_cloudinary(public_id: str):
    cloudinary.uploader.destroy(public_id)
