from typing import Iterable
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

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
        user_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        users: Iterable[User] = await user_repository.get_all_user()
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return GetUsersResponseSchema.from_entity(users)


@router.get(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponseSchema,
    description="Получение пользователя по логину",
)
async def get_user(
    login: str, container: Container = Depends(init_container)
) -> GetUserResponseSchema:
    try:
        user_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        user: User = await user_repository.get_user_by_login(login=login)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return GetUserResponseSchema.from_entity(user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GetUserResponseSchema,
    description="Добавление пользователя",
)
async def add_user(
    user_data: AddNewUserRequestSchema, container: Container = Depends(init_container)
) -> GetUserResponseSchema:
    try:
        user_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        user: User = User(user_data.login, user_data.password)
        await user_repository.add_user(user)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return GetUserResponseSchema.from_entity(user)
