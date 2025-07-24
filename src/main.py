from fastapi import FastAPI

from exception_handler import register_exception_handler
from routers import admin, auth, category, product, supplier, purchase

app = FastAPI()

register_exception_handler(app)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(supplier.router)
app.include_router(purchase.router)
