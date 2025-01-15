from dataclasses import dataclass

from application.common.interactor import Interactor
from application.user.dto import UserDTO
from domain.entities.user import User
from infrastructure.repository.base import BaseUserRepository


@dataclass
class GetUserInteractor(Interactor[UserDTO, User]):
    users_repository: BaseUserRepository

    async def __call__(self, user_dto: UserDTO) -> User:
        user: User = await self.users_repository.get_user_by_login(login=user_dto.login)
        return user
