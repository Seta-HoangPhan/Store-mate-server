from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from exception_handler import register_exception_handler
from routers import admin, auth, category, product, supplier, purchase

app = FastAPI()

register_exception_handler(app)

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(admin.router)
api_router.include_router(category.router)
api_router.include_router(product.router)
api_router.include_router(supplier.router)
api_router.include_router(purchase.router)

app.include_router(api_router)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
