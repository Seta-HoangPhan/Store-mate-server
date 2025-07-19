from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from response import err_msg, exception_res
from settings import settings

security = HTTPBearer()


def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.access_token_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return exception_res.unauthorized(err_msg.INVALID_TOKEN)
