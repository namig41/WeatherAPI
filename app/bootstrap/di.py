from functools import (
    lru_cache,
    partial,
)
from smtplib import SMTP

from aioredis import Redis
from punq import (
    Container,
    Scope,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from application.auth.login_user import LoginUserInteractor
from application.auth.validate_token import ValidateTokenInteractor
from application.location.add_location import AddLocationInteractor
from application.location.delete_location import DeleteLocationInteractor
from application.location.get_all_location import GetAllLocationInteractor
from application.location.get_location import GetLocationInteractor
from application.user.add_user import AddUserInteractor
from application.user.delete_user import DeleteUserInteractor
from application.user.get_all_user import GetAllUserInteractor
from application.user.get_user import GetUserInteractor
from application.weather.get_weather import GetWeatherInteractor
from domain.interfaces.infrastructure.access_service import IAuthAccessService
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from infrastructure.auth.access_service import PasswordAuthService
from infrastructure.auth.access_service_api import AuthServiceAPI
from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.auth.config import AuthConfig
from infrastructure.auth.password_hasher import SHA256PasswordHasher
from infrastructure.cache.base import ICacheWeatherService
from infrastructure.cache.config import CacheConfig
from infrastructure.cache.redis import (
    init_redis,
    RedisCacheWeatherService,
)
from infrastructure.database.config import DBConfig
from infrastructure.database.init import init_database
from infrastructure.email.base import IEmailClientService
from infrastructure.email.config import SMTPConfig
from infrastructure.email.email_client import SMTPEmailClient
from infrastructure.email.email_config_factory import ConfirmationEmailConfigFactory
from infrastructure.email.init import init_smtp_client
from infrastructure.jwt.base import BaseJWTProcessor
from infrastructure.jwt.config import JWTConfig
from infrastructure.jwt.jwt_processor import PyJWTProcessor
from infrastructure.logger.base import ILogger
from infrastructure.logger.logger import create_logger_dependency
from infrastructure.message_broker.config import EventBusConfig
from infrastructure.repository.base import (
    BaseUserLocationRepository,
    BaseUserRepository,
)
from infrastructure.repository.postgres import (
    PostgreSQLUserLocationRepository,
    PostgreSQLUserRepository,
)
from infrastructure.weather.base import IWeatherAPIService
from infrastructure.weather.config import WeatherAPIConfig
from infrastructure.weather.open_weather_api import OpenWeatherAPIService
from settings.config import (
    config,
    Settings,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container: Container = Container()

    container.register(
        Settings,
        instance=config,
        scope=Scope.singleton,
    )

    jwt_config: JWTConfig = JWTConfig()

    container.register(
        JWTConfig,
        instance=jwt_config,
        scope=Scope.singleton,
    )

    container.register(
        ILogger,
        factory=create_logger_dependency,
        scope=Scope.singleton,
    )

    event_bus_config: EventBusConfig = EventBusConfig()

    container.register(
        EventBusConfig,
        instance=event_bus_config,
        scope=Scope.singleton,
    )

    container.register(
        AsyncEngine,
        factory=partial(init_database, db_config=DBConfig()),
        scope=Scope.singleton,
    )

    container.register(
        BaseUserRepository,
        PostgreSQLUserRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseUserLocationRepository,
        PostgreSQLUserLocationRepository,
        scope=Scope.singleton,
    )

    container.register(
        AuthConfig,
        instance=AuthConfig(),
        scope=Scope.singleton,
    )

    container.register(
        AuthServiceAPI,
        scope=Scope.singleton,
    )

    container.register(
        IPasswordHasher,
        SHA256PasswordHasher,
        scope=Scope.singleton,
    )

    container.register(
        IAuthAccessService,
        PasswordAuthService,
        scope=Scope.singleton,
    )

    container.register(
        BaseJWTProcessor,
        PyJWTProcessor,
        scope=Scope.singleton,
    )

    container.register(
        AccessTokenProcessor,
        scope=Scope.singleton,
    )

    container.register(
        WeatherAPIConfig,
        instance=WeatherAPIConfig(),
        scope=Scope.singleton,
    )

    container.register(
        IWeatherAPIService,
        OpenWeatherAPIService,
        scope=Scope.singleton,
    )

    container.register(
        Redis,
        factory=partial(init_redis, cache_config=CacheConfig()),
        scope=Scope.singleton,
    )

    container.register(
        ICacheWeatherService,
        RedisCacheWeatherService,
        scope=Scope.singleton,
    )

    smtp_config: SMTPConfig = SMTPConfig()

    container.register(
        SMTPConfig,
        instance=smtp_config,
        scope=Scope.singleton,
    )

    container.register(
        ConfirmationEmailConfigFactory,
        scope=Scope.singleton,
    )

    container.register(
        SMTP,
        factory=partial(init_smtp_client, smtp_config=smtp_config),
        scope=Scope.singleton,
    )

    container.register(
        IEmailClientService,
        SMTPEmailClient,
        scope=Scope.singleton,
    )

    # AUTH UseCase
    container.register(LoginUserInteractor)
    container.register(ValidateTokenInteractor)

    # User UseCase
    container.register(AddUserInteractor)
    container.register(DeleteUserInteractor)
    container.register(GetUserInteractor)
    container.register(GetAllUserInteractor)

    # Location UseCase
    container.register(AddLocationInteractor)
    container.register(DeleteLocationInteractor)
    container.register(GetLocationInteractor)
    container.register(GetAllLocationInteractor)

    # Weather UseCase
    container.register(GetWeatherInteractor)
    return container
