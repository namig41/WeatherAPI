from dataclasses import dataclass

import httpx
from httpx import Response

from application.auth.dto import AccessTokenDTO
from application.user.dto import UserDTO
from domain.entities.user import User
from domain.value_objects.hashed_password import HashedPassword
from infrastructure.auth.config import AuthConfig
from infrastructure.exceptions.auth import AuthServiceException


@dataclass
class AuthServiceAPI:
    config: AuthConfig

    async def validate_token(self, token: str) -> User:
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(
                "http://auth_service_app:8000/auth/validate_token",
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

    async def login(self, user_dto: UserDTO) -> AccessTokenDTO:
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(
                "http://auth_service_app:8000/auth/login",
                data={"username": user_dto.login, "password": user_dto.password},
            )

            if response.status_code != 200:
                raise AuthServiceException()

            token: dict = response.json()
            return AccessTokenDTO(
                jwt_token=token["jwt_token"],
            )

    async def logout(self) -> None:
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(
                "http://auth_service_app:8000/auth/logout",
            )

            if response.status_code != 200:
                raise AuthServiceException()
