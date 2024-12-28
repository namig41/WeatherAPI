from dataclasses import dataclass

from application.common.interactor import Interactor
from domain.entities.user import User
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail
from infrastructure.email.base import IEmailClientService
from infrastructure.email.email_config_factory import (
    ConfirmationEmailConfigFactory,
    EmailMessageType,
)
from infrastructure.email.services.user import send_user_registration_email
from infrastructure.repository.base import BaseUserRepository
from presentation.api.auth_service.user.schema import AddNewUserRequestSchema


@dataclass
class AddUserInteractor(Interactor[AddNewUserRequestSchema, User]):
    users_repository: BaseUserRepository
    hasher_password: IPasswordHasher
    email_service: IEmailClientService
    confirmation_email_config: ConfirmationEmailConfigFactory

    async def __call__(self, user_add_schema: AddNewUserRequestSchema) -> User:
        await self.users_repository.user_exists(user_add_schema.login)

        user: User = User.create_with_raw_password(
            user_add_schema.login,
            UserEmail(user_add_schema.email),
            RawPassword(user_add_schema.password),
            self.hasher_password,
        )
        await self.users_repository.add_user(user)

        await send_user_registration_email(
            user,
            self.confirmation_email_config.create(EmailMessageType.REGISTRATION),
            self.email_service,
        )

        return user
