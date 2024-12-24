from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import JSONResponse

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
)
from infrastructure.jwt.base import JWTToken
from infrastructure.repository.base import BaseUserRepository
from punq import Container

from application.api.auth.schema import (
    GetMeResponseSchema,
    LoginUserRequestSchema,
)
from application.di.container import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from domain.interfaces.infrastructure.access_service import IAuthAccessService
from domain.value_objects.raw_password import RawPassword


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Авторизация пользователя",
)
async def login_user(
    user_data: LoginUserRequestSchema,
    response: Response,
    container: Container = Depends(init_container),
) -> JSONResponse:
    try:
        auth_access_service: IAuthAccessService = container.resolve(IAuthAccessService)
        access_token_processor: AccessTokenProcessor = container.resolve(
            AccessTokenProcessor,
        )
        await auth_access_service.authorize(
            user_data.login,
            RawPassword(user_data.password),
        )
        # TODO: Придумать более гибкое формирование полезной нагрузки jwt
        payload: JWTPayload = JWTPayload.from_dict({"login": user_data.login})
        access_token: AccessToken = AccessToken.create_with_expiration(payload)
        jwt_token: JWTToken = access_token_processor.encode(access_token)
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            samesite="lax",
            secure=False,
        )
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        # TODO: Лишний запрос в базу данных. Возможно стоит добавить email в jwt
        user: User = await users_repository.get_user_by_login(user_data.login)
        email_service: IEmailClientService = container.resolve(IEmailClientService)
        await send_user_authorization_email(
            user,
            ConfirmationEmailConfigFactory.create(EmailMessageType.AUTHORIZATION),
            email_service,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return JSONResponse(content={"access_token": jwt_token})


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Выход пользователя из системы",
)
async def logout_user(response: Response) -> JSONResponse:
    response.delete_cookie(key="access_token")
    return JSONResponse(content={"message": "Вы успешно вышли из системы."})


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=GetMeResponseSchema,
    description="Получение информации о текущем пользователе",
)
async def me(
    jwt_token: JWTToken = Cookie(None, alias="access_token"),
    container: Container = Depends(init_container),
) -> GetMeResponseSchema:
    try:
        users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
        access_token_processor: AccessTokenProcessor = container.resolve(
            AccessTokenProcessor,
        )
        access_token: AccessToken = access_token_processor.decode(jwt_token)
        user: User = await users_repository.get_user_by_login(
            login=access_token.payload.login,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return GetMeResponseSchema.from_entity(user)
