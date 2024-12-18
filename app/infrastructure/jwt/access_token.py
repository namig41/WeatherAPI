from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import (
    Any,
    TypeAlias,
)

from infrastructure.exceptions.jwt import JWTExpiredException

from domain.entities.base import BaseEntity


JWTPayloadDict: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


@dataclass
class JWTPayload:
    login: str

    def to_dict(self) -> JWTPayloadDict:
        return {
            "login": self.login,
        }

    @classmethod
    def from_dict(cls, payload_dict: JWTPayloadDict):
        return cls(
            login=payload_dict["login"],
        )


@dataclass
class AccessToken(BaseEntity):
    payload: JWTPayload
    expires_in: datetime

    def validate(self) -> None:
        if datetime.now(timezone.utc) > self.expires_in:
            raise JWTExpiredException()

    @classmethod
    def create_with_expiration(
        cls, payload: JWTPayload, minutes: int = 5,
    ) -> "AccessToken":
        return cls(
            payload=payload,
            expires_in=datetime.now(timezone.utc) + timedelta(minutes=minutes),
        )

    @classmethod
    def from_payload_dict(
        cls, payload_dict: JWTPayloadDict, minutes: int = 5,
    ) -> "AccessToken":
        payload = JWTPayload.from_dict(payload_dict)
        return cls.create_with_expiration(payload=payload, minutes=minutes)
