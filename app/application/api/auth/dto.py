from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
    timezone,
)


@dataclass(frozen=True)
class AccessTokenDTO:
    login: str
    expires_in: datetime

    @classmethod
    def create_expiring_token(cls, login: str, minutes: int = 30) -> "AccessTokenDTO":
        return cls(
            login=login,
            expires_in=datetime.now(timezone.utc) + timedelta(minutes=minutes),
        )
