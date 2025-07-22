from cloudinary.exceptions import Error as CloudinaryErr
from fastapi import FastAPI, Request

from response import err_msg, exception_res


def register_exception_handler(app: FastAPI):
    @app.exception_handler(CloudinaryErr)
    async def handle_cloudinary_exception(request: Request, exc: Exception):
        print("cloudinary err ", exc)
        return exception_res.internal_error(err_msg.UPLOAD_CLOUDINARY_FAILED)

    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        print("general err ", exc)
        return exception_res.internal_error(err_msg.INTERNAL_SERVER_ERR)
