from dataclasses import dataclass

from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from domain.interfaces.infrastructure.access_service import IAuthAccessService
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from infrastructure.exceptions.auth import UserAuthFailedException
from infrastructure.repository.base import BaseUserRepository


@dataclass
class PasswordAuthService(IAuthAccessService):
    users_repository: BaseUserRepository
    password_hasher: IPasswordHasher

    async def authorize(self, login: str, raw_password: RawPassword) -> None:
        try:
            user: User = await self.users_repository.get_user_by_login(login=login)
            if not self.password_hasher.verify_password(
                raw_password,
                user.hashed_password,
            ):
                raise UserAuthFailedException()
        except ApplicationException:
            raise
