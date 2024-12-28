from dataclasses import dataclass

from fastapi import Request

import httpx

from domain.entities.user import User
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.user_email import UserEmail
from infrastructure.auth.config import AuthConfig
from infrastructure.exceptions.auth import (
    AuthServiceException,
    TokenMissingException,
)
from infrastructure.jwt.access_token import JWTToken


@dataclass
class AuthServiceAPI:
    config: AuthConfig

    async def validate_token(self, request: Request) -> User:
        token: JWTToken | None = request.headers.get("Authorization")
        if not token:
            raise TokenMissingException()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.config.get_url()}/auth/validate_token",
                headers={"Authorization": token},
            )
            if response.status_code != 200:
                raise AuthServiceException
            user_data: dict = response.json()

            return User(
                login=user_data["login"],
                email=UserEmail(user_data["email"]),
                hashed_password=HashedPassword(user_data["password"]),
            )
