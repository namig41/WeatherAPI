from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from application.user.add_user import AddUserInteractor
from application.user.delete_user import DeleteUserInteractor
from application.user.dto import UserDTO
from application.user.get_all_user import GetAllUserInteractor
from application.user.get_user import GetUserInteractor
from bootstrap.di import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from presentation.api.auth_service.v1.user.schema import (
    AddNewUserRequestSchema,
    GetUserResponseSchema,
    GetUsersResponseSchema,
)
from presentation.api.common.filters import FiltersSchema


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=GetUsersResponseSchema,
    description="Получение всех пользователей",
)
async def get_all_user(
    filters_schema: FiltersSchema = Depends(),
    container: Container = Depends(init_container),
) -> GetUsersResponseSchema:
    try:
        get_all_user_action: GetAllUserInteractor = container.resolve(
            GetAllUserInteractor,
        )
        users: Iterable[User] = await get_all_user_action(
            filters_schema.to_repository_filters(),
        )
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
        user_dto: UserDTO = UserDTO(login=login)
        get_user_action: GetUserInteractor = container.resolve(GetUserInteractor)
        user: User = await get_user_action(user_dto)
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
        user_dto: UserDTO = UserDTO(
            login=user_data.login,
            email=user_data.email,
            password=user_data.password,
        )
        add_user_action: AddUserInteractor = container.resolve(AddUserInteractor)
        user: User = await add_user_action(user_dto)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUserResponseSchema.from_entity(user)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление пользователя",
)
async def delete_user(
    login: str,
    container: Container = Depends(init_container),
) -> None:
    try:
        user_dto: UserDTO = UserDTO(login=login)
        user_delete_action: DeleteUserInteractor = container.resolve(
            DeleteUserInteractor,
        )
        await user_delete_action(user_dto)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
