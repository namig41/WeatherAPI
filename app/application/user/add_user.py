from dataclasses import dataclass

from application.common.interactor import Interactor
from application.user.dto import UserDTO
from domain.entities.user import User
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail
from infrastructure.email.base import IEmailClientService
from infrastructure.email.email_config_factory import ConfirmationEmailConfigFactory
from infrastructure.message_broker.message import Message
from infrastructure.message_broker.producer.user import UserProducer
from infrastructure.repository.base import BaseUserRepository
from infrastructure.task_queue.email_tasks.user import send_user_confirmation_email


@dataclass
class AddUserInteractor(Interactor[UserDTO, User]):
    users_repository: BaseUserRepository
    hasher_password: IPasswordHasher
    email_service: IEmailClientService
    confirmation_email_config: ConfirmationEmailConfigFactory
    user_producer: UserProducer

    async def __call__(self, user_dto: UserDTO) -> User:
        await self.users_repository.user_exists(user_dto.login)

        user: User = User.create_with_raw_password(
            login=user_dto.login,
            email=UserEmail(user_dto.email),
            raw_password=RawPassword(user_dto.password),
            password_hasher=self.hasher_password,
        )
        await self.users_repository.add_user(user)

        send_user_confirmation_email.delay(
            user.login,
            user.email.to_raw(),
        )

        message: Message = Message(
            data=user.login,
        )

        await self.user_producer.publish(message)

        return user
