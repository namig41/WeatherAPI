from fastapi import (
    Request,
    Response,
)

from punq import Container
from sqladmin.authentication import AuthenticationBackend

from bootstrap.di import init_container
from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.jwt.access_token import (
    AccessToken,
    JWTPayload,
)
from infrastructure.jwt.jwt_processor import JWTToken
from settings.config import config


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        container: Container = init_container()
        access_token_processor: AccessTokenProcessor = container.resolve(
            AccessTokenProcessor,
        )

        form = await request.form()
        username, password = form["username"], form["password"]

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            payload: JWTPayload = JWTPayload.from_dict(
                {"user_id": hash(password), "login": username},
            )
            access_token: AccessToken = AccessToken.create_with_expiration(
                payload, minutes=30,
            )
            jwt_token: JWTToken = access_token_processor.encode(access_token)
            request.session.update({"token": jwt_token})

            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(
        self,
        request: Request,
    ) -> Response | bool:
        container: Container = init_container()
        access_token_processor: AccessTokenProcessor = container.resolve(
            AccessTokenProcessor,
        )

        jwt_token: JWTToken | None = request.session.get("token")
        if jwt_token is None:
            return False

        access_token: AccessToken = access_token_processor.decode(jwt_token)
        if access_token.payload.login != config.ADMIN_USERNAME:
            return False

        return True
