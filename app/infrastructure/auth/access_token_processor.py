from dataclasses import dataclass
from datetime import datetime

from infrastructure.jwt.base import (
    BaseJWTProcessor,
    JWTPayload,
    JWTToken,
)

from application.api.auth.dto import AccessTokenDTO
from application.api.exceptions.user import UserAuthFailedException


@dataclass
class AccessTokenProcessor:
    jwt_processor: BaseJWTProcessor

    def encode(
        self,
        token: AccessTokenDTO,
    ) -> JWTToken:
        jwt_token_payload: JWTPayload = {
            "sub": {"login": token.login},
            "exp": token.expires_in,
        }
        encoded_jwt = self.jwt_processor.encode(jwt_token_payload)
        return encoded_jwt

    def decode(self, token: JWTToken) -> AccessTokenDTO:
        try:
            payload = self.jwt_processor.decode(token)
            sub = payload["sub"]

            login = sub["login"]
            expires_in = datetime.fromtimestamp(float(payload["exp"]))
            access_token = AccessTokenDTO(
                login=login,
                expires_in=expires_in,
            )

            return access_token
        except (ValueError, TypeError, KeyError):
            raise UserAuthFailedException()
