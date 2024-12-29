from dataclasses import dataclass

import httpx

from domain.entities.user import User
from domain.value_objects.hashed_password import HashedPassword
from infrastructure.auth.config import AuthConfig
from infrastructure.exceptions.auth import AuthServiceException


@dataclass
class AuthServiceAPI:
    config: AuthConfig

    async def validate_token(self, token: str) -> User:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.config.get_url()}/auth/validate_token",
                headers={"Authorization": f"Bearer {token}"},
            )

            if response.status_code != 200:
                raise AuthServiceException()

            user_data: dict = response.json()
            return User(
                login=user_data["login"],
                email=user_data["email"],
                hashed_password=HashedPassword(user_data["password"]),
            )
