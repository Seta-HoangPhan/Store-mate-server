from fastapi import FastAPI
from exception_handler import register_exception_handler

app = FastAPI()

register_exception_handler(app)
