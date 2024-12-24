from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from infrastructure.email.base import IEmailClientService
from infrastructure.email.email_config_factory import (
    ConfirmationEmailConfigFactory,
    EmailMessageType,
)
from infrastructure.email.services.user import send_user_registration_email
from infrastructure.repository.base import BaseUserRepository
from punq import Container

from application.api.user.schema import (
    AddNewUserRequestSchema,
    GetUserResponseSchema,
    GetUsersResponseSchema,
)
from application.di.container import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail


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
        hasher_password: IPasswordHasher = container.resolve(IPasswordHasher)
        user: User = User.create_with_raw_password(
            user_data.login,
            UserEmail(user_data.email),
            RawPassword(user_data.password),
            hasher_password,
        )
        await users_repository.add_user(user)

        email_service: IEmailClientService = container.resolve(IEmailClientService)
        await send_user_registration_email(
            user,
            ConfirmationEmailConfigFactory.create(EmailMessageType.REGISTRATION),
            email_service,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetUserResponseSchema.from_entity(user)
