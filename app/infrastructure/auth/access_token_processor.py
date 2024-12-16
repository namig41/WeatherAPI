from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
    timezone,
)

from infrastructure.jwt.base import (
    BaseJWTProcessor,
    JWTPayload,
    JWTToken,
)


@dataclass
class AccessTokenProcessor:
    jwt_processor: BaseJWTProcessor

    def create_access_token(
        self, jwt_payload: JWTPayload, minutes: int = 30,
    ) -> JWTToken:
        to_encode = jwt_payload.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        to_encode.update({"exp": expire.isoformat()})
        encoded_jwt = self.jwt_processor.encode(to_encode)
        return encoded_jwt
