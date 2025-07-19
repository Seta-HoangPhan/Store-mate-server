from fastapi import FastAPI

from exception_handler import register_exception_handler
from routers import admin, auth

app = FastAPI()

register_exception_handler(app)

app.include_router(auth.router)
app.include_router(admin.router)
