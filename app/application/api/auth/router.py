from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import JSONResponse

from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.jwt.base import JWTToken
from infrastructure.repository.base import BaseUserRepository
from presenter.di.container import init_container
from punq import Container

from application.api.auth.dto import AccessTokenDTO
from application.api.user.schema import GetUserResponseSchema
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from domain.interfaces.infrastructure.access_service import BaseAccessService
from domain.value_objects.raw_password import RawPassword


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Авторизация пользователя",
)
async def login_user(
    user_data: GetUserResponseSchema,
    response: Response,
    container: Container = Depends(init_container),
) -> JSONResponse:
    try:
        auth_access_service: BaseAccessService = container.resolve(BaseAccessService)
        access_token_processor: AccessTokenProcessor = container.resolve(
            AccessTokenProcessor,
        )
        login: str = user_data.login
        raw_password: RawPassword = RawPassword(user_data.password)
        await auth_access_service.authorize(login, raw_password)
        access_token_dto: AccessTokenDTO = AccessTokenDTO.create_expiring_token(login)
        access_token: JWTToken = access_token_processor.encode(access_token_dto)
        response.set_cookie("access_token", access_token, httponly=True)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return JSONResponse(content={"access_token": access_token})


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Выход пользователя из системы",
)
async def logout_user(response: Response) -> JSONResponse:
    response.delete_cookie("access_token")
    return JSONResponse(content={"message": "Вы успешно вышли из системы."})


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponseSchema,
    description="Получение информации о текущем пользователе",
)
async def me(
    access_token: str = Cookie(None, alias="access_token"),
    container: Container = Depends(init_container),
) -> GetUserResponseSchema:
    try:
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        access_token_processor: AccessTokenProcessor = container.resolve(
            AccessTokenProcessor,
        )
        access_token_dto: AccessTokenDTO = access_token_processor.decode(access_token)
        user: User = await users_repository.get_user_by_login(
            login=access_token_dto.login,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUserResponseSchema.from_entity(user)
