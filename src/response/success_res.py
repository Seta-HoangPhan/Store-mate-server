from fastapi.responses import JSONResponse
from starlette import status


def ok(detail: str = None, data=None):
    content = {}

    if detail is not None:
        content["detail"] = detail

    if data is not None:
        content["data"] = data

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


def create(detail: str, data):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"data": data, "detail": detail}
    )
