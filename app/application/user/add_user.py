from dataclasses import dataclass

from application.common.interactor import Interactor
from application.user.dto import UserDTO
from domain.entities.user import User
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail
from infrastructure.email.base import IEmailClientService
from infrastructure.email.email_config_factory import ConfirmationEmailConfigFactory
from infrastructure.repository.base import BaseUserRepository
from infrastructure.task_queue.email_tasks.user import send_user_confirmation_email


@dataclass
class AddUserInteractor(Interactor[UserDTO, User]):
    users_repository: BaseUserRepository
    hasher_password: IPasswordHasher
    email_service: IEmailClientService
    confirmation_email_config: ConfirmationEmailConfigFactory

    async def __call__(self, user_dto: UserDTO) -> User:
        await self.users_repository.user_exists(user_dto.login)

        user: User = User.create_with_raw_password(
            user_dto.login,
            UserEmail(user_dto.email),
            RawPassword(user_dto.password),
            self.hasher_password,
        )
        await self.users_repository.add_user(user)

        send_user_confirmation_email.delay(
            user.login,
            user.email.to_raw(),
        )

        return user
