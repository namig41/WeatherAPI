from dataclasses import dataclass

from application.auth.dto import AccessTokenDTO
from application.common.interactor import Interactor
from domain.entities.user import User
from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.jwt.access_token import AccessToken
from infrastructure.repository.base import BaseUserRepository


@dataclass
class ValidateTokenInteractor(Interactor[AccessTokenDTO, User]):

    access_token_processor: AccessTokenProcessor
    users_repository: BaseUserRepository

    async def __call__(self, access_token_dto: AccessTokenDTO) -> User:
        access_token: AccessToken = self.access_token_processor.decode(
            access_token_dto.jwt_token,
        )
        user: User = await self.users_repository.get_user_by_login(
            login=access_token.payload.login,
        )
        return user
