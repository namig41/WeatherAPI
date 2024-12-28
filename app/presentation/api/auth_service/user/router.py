from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from application.common.interactor import Interactor
from bootstrap.di import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infrastructure.repository.base import BaseUserRepository
from presentation.api.auth_service.user.schema import (
    AddNewUserRequestSchema,
    GetUserResponseSchema,
    GetUsersResponseSchema,
)


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
    "/{login}",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponseSchema,
    description="Авторизация и выдача токена",
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
    description="Регистрация нового пользователя",
)
async def add_user(
    user_data: AddNewUserRequestSchema,
    container: Container = Depends(init_container),
) -> GetUserResponseSchema:
    try:
        add_user_action: Interactor[AddNewUserRequestSchema, User] = container.resolve(
            Interactor[AddNewUserRequestSchema, User],
        )

        user: User = await add_user_action(user_data)

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUserResponseSchema.from_entity(user)
