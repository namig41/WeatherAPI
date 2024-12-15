from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import JSONResponse

from punq import Container

from application.api.user.auth import (
    authenticate_user,
    create_access_token,
    verify_plain_password,
)
from application.api.user.schema import (
    AddNewUserRequestSchema,
    GetUserResponseSchema,
    GetUsersResponseSchema,
)
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infra.container.init import init_container
from infra.repository.base import BaseUserRepository


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=GetUsersResponseSchema,
    description="Получение всех пользователей",
)
async def get_all_user(
    container: Container = Depends(init_container),
) -> GetUsersResponseSchema:
    try:
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        users: Iterable[User] = await users_repository.get_all_user()
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUsersResponseSchema.from_entity(users)


@router.get(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponseSchema,
    description="Получение пользователя по логину",
)
async def get_user(
    login: str,
    container: Container = Depends(init_container),
) -> GetUserResponseSchema:
    try:
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        user: User = await users_repository.get_user_by_login(login=login)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUserResponseSchema.from_entity(user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GetUserResponseSchema,
    description="Добавление пользователя",
)
async def add_user(
    user_data: AddNewUserRequestSchema,
    container: Container = Depends(init_container),
) -> GetUserResponseSchema:
    try:
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        user: User = User(user_data.login, user_data.password)
        await users_repository.add_user(user)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUserResponseSchema.from_entity(user)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Авторизация пользователя",
)
async def login_user(
    user_data: GetUserResponseSchema,
    response: Response,
    container: Container = Depends(init_container),
):
    try:
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        user: User = User(user_data.login, user_data.password)
        user = await authenticate_user(user, users_repository, verify_plain_password)
        access_token = create_access_token({"sub": str(user.login)})
        response.set_cookie("access_token", access_token, httponly=True)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return {"access_token": access_token}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Выход пользователя из системы",
)
async def logout_user(response: Response) -> JSONResponse:
    try:
        response.delete_cookie("access_token")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Не удалось удалить cookie."},
        )
    return JSONResponse(content={"message": "Вы успешно вышли из системы."})
