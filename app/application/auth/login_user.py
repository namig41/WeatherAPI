from dataclasses import dataclass

from application.auth.dto import AccessTokenDTO
from application.common.interactor import Interactor
from application.user.dto import UserDTO
from domain.entities.user import User
from domain.interfaces.infrastructure.access_service import IAuthAccessService
from domain.value_objects.raw_password import RawPassword
from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.email.base import IEmailClientService
from infrastructure.email.email_config_factory import ConfirmationEmailConfigFactory
from infrastructure.jwt.access_token import (
    AccessToken,
    JWTPayload,
    JWTToken,
)
from infrastructure.repository.base import BaseUserRepository


@dataclass
class LoginUserInteractor(Interactor[UserDTO, AccessTokenDTO]):

    auth_access_service: IAuthAccessService
    access_token_processor: AccessTokenProcessor
    users_repository: BaseUserRepository
    email_service: IEmailClientService
    confirmation_email_config: ConfirmationEmailConfigFactory

    async def __call__(self, user_dto: UserDTO) -> AccessTokenDTO:
        await self.auth_access_service.authorize(
            login=user_dto.login,
            raw_password=RawPassword(user_dto.password),
        )

        user: User = await self.users_repository.get_user_by_login(user_dto.login)

        payload: JWTPayload = JWTPayload.from_dict(
            {"user_id": user.id, "login": user_dto.login},
        )
        access_token: AccessToken = AccessToken.create_with_expiration(payload)
        jwt_token: JWTToken = self.access_token_processor.encode(access_token)

        return AccessTokenDTO(jwt_token=jwt_token, type="Bearer")
