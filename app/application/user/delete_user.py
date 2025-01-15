from dataclasses import dataclass

from application.common.interactor import Interactor
from application.user.dto import UserDTO
from infrastructure.repository.base import BaseUserRepository


@dataclass
class DeleteUserInteractor(Interactor[UserDTO, None]):
    users_repository: BaseUserRepository

    async def __call__(self, user_dto: UserDTO) -> None:
        await self.users_repository.user_exists(login=user_dto.login)
        await self.users_repository.delete_user_by_login(login=user_dto.login)
