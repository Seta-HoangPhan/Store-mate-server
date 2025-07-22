from fastapi import HTTPException, status


def bad_request(detail: str = "Bad request"):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def unauthorized(detail: str = "Unauthorized"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def payment_required(detail: str = "Payment Required"):
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)


def forbidden(detail: str = "Forbidden"):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def not_found(detail: str = "Not found"):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def conflict(detail: str = "Conflict"):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def internal_error(detail: str = "Internal server error"):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
    )
