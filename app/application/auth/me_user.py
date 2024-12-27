from dataclasses import dataclass

from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.jwt.access_token import (
    AccessToken,
    JWTToken,
)
from infrastructure.repository.base import BaseUserRepository

from application.common.interactor import Interactor
from domain.entities.user import User


@dataclass
class MeUserInteractor(Interactor[JWTToken, User]):

    access_token_processor: AccessTokenProcessor
    users_repository: BaseUserRepository

    async def __call__(self, jwt_token: JWTToken) -> User:
        access_token: AccessToken = self.access_token_processor.decode(jwt_token)
        user: User = await self.users_repository.get_user_by_login(
            login=access_token.payload.login,
        )

        return user
