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


def upload_image_to_cloudinary(file: UploadFile) -> str:
    result = cloudinary.uploader.upload(file.file)
    return result.get("secure_url")
