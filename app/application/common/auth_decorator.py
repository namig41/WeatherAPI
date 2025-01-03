from functools import wraps

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

from bootstrap.di import init_container
from domain.exceptions.base import ApplicationException
from infrastructure.auth.access_service_api import AuthServiceAPI


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def validate_token_decorator(func):
    @wraps(func)
    async def wrapper(
        *args,
        token: str = Depends(oauth2_scheme),
        container=Depends(init_container),
        **kwargs,
    ):
        auth_service_api = container.resolve(AuthServiceAPI)
        try:
            user = await auth_service_api.validate_token(token)
        except ApplicationException as exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": exception.message},
            )
        return await func(*args, user=user, container=container, **kwargs)

    return wrapper
