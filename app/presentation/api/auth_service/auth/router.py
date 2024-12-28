from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import JSONResponse

from punq import Container

from application.common.interactor import Interactor
from bootstrap.di import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infrastructure.jwt.access_token import JWTToken
from presentation.api.auth_service.auth.schema import (
    GetMeResponseSchema,
    LoginUserRequestSchema,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Авторизация пользователя",
)
async def login_user(
    user_data: LoginUserRequestSchema,
    response: Response,
    container: Container = Depends(init_container),
) -> JSONResponse:
    try:
        login_user_action: Interactor[LoginUserRequestSchema, JWTToken] = (
            container.resolve(
                Interactor[LoginUserRequestSchema, JWTToken],
            )
        )

        jwt_token: JWTToken = await login_user_action(user_data)

        response.set_cookie(
            key="access_token",
            value=jwt_token,
            samesite="lax",
            secure=False,
        )

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )

    return JSONResponse(content={"access_token": jwt_token})


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Завершение сессии",
)
async def logout_user(response: Response) -> JSONResponse:
    response.delete_cookie(key="access_token")
    return JSONResponse(content={"message": "Вы успешно вышли из системы."})


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=GetMeResponseSchema,
    description="Получение информации о текущем пользователе",
)
async def me(
    jwt_token: JWTToken = Cookie(None, alias="access_token"),
    container: Container = Depends(init_container),
) -> GetMeResponseSchema:
    try:
        me_user_action: Interactor[JWTToken, User] = container.resolve(
            Interactor[JWTToken, User],
        )

        user: User = await me_user_action(jwt_token)

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetMeResponseSchema.from_entity(user)


@router.get(
    "/validate_token",
    status_code=status.HTTP_200_OK,
    response_model=GetMeResponseSchema,
    description="Проверка токена",
)
async def validate_token(
    jwt_token: JWTToken = Cookie(None, alias="access_token"),
    container: Container = Depends(init_container),
) -> GetMeResponseSchema:
    try:
        me_user_action: Interactor[JWTToken, User] = container.resolve(
            Interactor[JWTToken, User],
        )

        user: User = await me_user_action(jwt_token)

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetMeResponseSchema.from_entity(user)
