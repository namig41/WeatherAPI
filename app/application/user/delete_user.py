from dataclasses import dataclass

from application.common.interactor import Interactor
from application.user.dto import UserDataDTO
from infrastructure.repository.base import BaseUserRepository


@dataclass
class DeleteUserInteractor(Interactor[UserDataDTO, None]):
    users_repository: BaseUserRepository

    async def __call__(self, user_dto: UserDataDTO) -> None:
        await self.users_repository.user_exists(login=user_dto.login)
        await self.users_repository.delete_user_by_login(login=user_dto.login)
