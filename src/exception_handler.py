from fastapi import FastAPI, Request
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError

from response import err_msg, exception_res


def register_exception_handler(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def handle_integrity_err(req: Request, exc: IntegrityError):
        if isinstance(exc.orig, UniqueViolation):
            return exception_res.conflict(err_msg.EMAIL_EXIST)

        if isinstance(exc.orig, ForeignKeyViolation):
            return exception_res.bad_request(err_msg.FOREIGN_KEY_VIOLATION)

        return exception_res.bad_request(err_msg.DB_ERR)

    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        return exception_res.internal_error(err_msg.INTERNAL_SERVER_ERR)
