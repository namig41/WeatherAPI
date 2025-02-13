from dataclasses import dataclass
from datetime import (
    datetime,
    timezone,
)

from domain.exceptions.base import ApplicationException
from infrastructure.exceptions.auth import UserAuthFailedException
from infrastructure.jwt.access_token import (
    AccessToken,
    JWTPayload,
)
from infrastructure.jwt.base import (
    BaseJWTProcessor,
    JWTPayloadDict,
    JWTToken,
)


@dataclass
class AccessTokenProcessor:
    jwt_processor: BaseJWTProcessor

    def encode(
        self,
        token: AccessToken,
    ) -> JWTToken:
        jwt_token_payload: JWTPayloadDict = {
            "sub": str(token.payload),
            "exp": token.expires_in,
        }
        return self.jwt_processor.encode(jwt_token_payload)

    def decode(self, token: JWTToken) -> AccessToken:
        try:
            jwt_token_payload: JWTPayloadDict = self.jwt_processor.decode(token)
            access_token = AccessToken(
                payload=JWTPayload.from_raw(jwt_token_payload["sub"]),
                expires_in=datetime.fromtimestamp(
                    jwt_token_payload["exp"],
                    tz=timezone.utc,
                ),
            )
            return access_token
        except ApplicationException:
            raise
        except (ValueError, TypeError, KeyError):
            raise UserAuthFailedException()
