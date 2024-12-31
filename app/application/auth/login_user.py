from dataclasses import dataclass

from application.auth.dto import AccessTokenDTO
from application.common.interactor import Interactor
from domain.entities.user import User
from domain.interfaces.infrastructure.access_service import IAuthAccessService
from domain.value_objects.raw_password import RawPassword
from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.email.base import IEmailClientService
from infrastructure.email.email_config_factory import (
    ConfirmationEmailConfigFactory,
    EmailMessageType,
)
from infrastructure.email.services.user import send_user_authorization_email
from infrastructure.jwt.access_token import (
    AccessToken,
    JWTPayload,
    JWTToken,
)
from infrastructure.repository.base import BaseUserRepository
from presentation.api.auth_service.auth.schema import LoginUserRequestSchema


@dataclass
class LoginUserInteractor(Interactor[LoginUserRequestSchema, AccessTokenDTO]):

    auth_access_service: IAuthAccessService
    access_token_processor: AccessTokenProcessor
    users_repository: BaseUserRepository
    email_service: IEmailClientService
    confirmation_email_config: ConfirmationEmailConfigFactory

    async def __call__(self, data: LoginUserRequestSchema) -> AccessTokenDTO:
        await self.auth_access_service.authorize(
            data.login,
            RawPassword(data.password),
        )

        user: User = await self.users_repository.get_user_by_login(data.login)

        payload: JWTPayload = JWTPayload.from_dict(
            {"user_id": user.id, "login": data.login},
        )
        access_token: AccessToken = AccessToken.create_with_expiration(payload)
        jwt_token: JWTToken = self.access_token_processor.encode(access_token)

        await send_user_authorization_email(
            user,
            self.confirmation_email_config.create(EmailMessageType.AUTHORIZATION),
            self.email_service,
        )

        return AccessTokenDTO(access_token=jwt_token, token_type="Bearer")
