from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from punq import Container

from application.auth.dto import AccessTokenDTO
from application.common.interactor import Interactor
from bootstrap.di import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infrastructure.jwt.access_token import JWTToken
from presentation.api.auth_service.v1.auth.schema import (
    GetMeResponseSchema,
    LoginUserRequestSchema,
)


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Авторизация пользователя",
)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  # type: ignore
    container: Container = Depends(init_container),
) -> AccessTokenDTO:
    try:
        user_data: LoginUserRequestSchema = LoginUserRequestSchema(
            login=form_data.username,
            password=form_data.password,
        )

        login_user_action: Interactor[LoginUserRequestSchema, AccessTokenDTO] = (
            container.resolve(
                Interactor[LoginUserRequestSchema, AccessTokenDTO],
            )
        )
        access_token: AccessTokenDTO = await login_user_action(user_data)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )

    return access_token


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Завершение сессии",
)
async def logout_user(response: Response) -> JSONResponse:
    response.delete_cookie(key="access_token")
    return JSONResponse(content={"message": "Вы успешно вышли из системы."})


@router.get(
    "/validate_token",
    status_code=status.HTTP_200_OK,
    response_model=GetMeResponseSchema,
    description="Проверка токена",
)
async def validate_token(
    token: JWTToken = Depends(oauth2_scheme),
    container: Container = Depends(init_container),
) -> GetMeResponseSchema:
    try:
        validate_token_action: Interactor[JWTToken, User] = container.resolve(
            Interactor[JWTToken, User],
        )
        user: User = await validate_token_action(token)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetMeResponseSchema.from_entity(user)
