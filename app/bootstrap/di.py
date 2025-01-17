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
from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.config import MessageBrokerConfig
from infrastructure.message_broker.message_broker import RabbitMQMessageBroker
from infrastructure.message_broker.message_broker_factory import (
    ChannelFactory,
    ConnectionFactory,
)
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


# Cache the initialization of the container to ensure singleton behavior
@lru_cache(1)
def init_container() -> Container:
    return _init_container()


# Initialize the dependency injection container
def _init_container() -> Container:
    container: Container = Container()

    # Register global settings
    container.register(
        Settings,
        instance=config,
        scope=Scope.singleton,
    )

    # Register logger
    container.register(
        ILogger,
        factory=create_logger_dependency,
        scope=Scope.singleton,
    )

    # Register message broker configuration
    message_broker_config: MessageBrokerConfig = MessageBrokerConfig()
    container.register(
        MessageBrokerConfig,
        instance=message_broker_config,
        scope=Scope.singleton,
    )

    # Register database configuration
    db_config: DBConfig = DBConfig()
    container.register(
        DBConfig,
        instance=db_config,
        scope=Scope.singleton,
    )

    # Register database engine
    container.register(
        AsyncEngine,
        factory=partial(init_database, db_config=db_config),
        scope=Scope.singleton,
    )

    # Register user repository
    container.register(
        BaseUserRepository,
        PostgreSQLUserRepository,
        scope=Scope.singleton,
    )

    # Register location repository
    container.register(
        BaseUserLocationRepository,
        PostgreSQLUserLocationRepository,
        scope=Scope.singleton,
    )

    # Register authentication configuration
    auth_config: AuthConfig = AuthConfig()
    container.register(
        AuthConfig,
        instance=auth_config,
        scope=Scope.singleton,
    )

    # Register authentication services
    container.register(
        AuthServiceAPI,
        scope=Scope.singleton,
    )

    # Register password hasher
    container.register(
        IPasswordHasher,
        SHA256PasswordHasher,
        scope=Scope.singleton,
    )

    # Register authentication access service
    container.register(
        IAuthAccessService,
        PasswordAuthService,
        scope=Scope.singleton,
    )

    # Register JWT configuration
    jwt_config: JWTConfig = JWTConfig()
    container.register(
        JWTConfig,
        instance=jwt_config,
        scope=Scope.singleton,
    )

    # Register JWT processor
    container.register(
        BaseJWTProcessor,
        PyJWTProcessor,
        scope=Scope.singleton,
    )

    # Register access token processor
    container.register(
        AccessTokenProcessor,
        scope=Scope.singleton,
    )

    # Register weather API configuration
    weather_config: WeatherAPIConfig = WeatherAPIConfig()
    container.register(
        WeatherAPIConfig,
        instance=weather_config,
        scope=Scope.singleton,
    )

    # Register weather API service
    container.register(
        IWeatherAPIService,
        OpenWeatherAPIService,
        scope=Scope.singleton,
    )

    # Register cache configuration
    cache_config: CacheConfig = CacheConfig()
    container.register(
        Redis,
        factory=partial(init_redis, cache_config=cache_config),
        scope=Scope.singleton,
    )

    # Register cache weather service
    container.register(
        ICacheWeatherService,
        RedisCacheWeatherService,
        scope=Scope.singleton,
    )

    # Register email configuration
    smtp_config: SMTPConfig = SMTPConfig()
    container.register(
        SMTPConfig,
        instance=smtp_config,
        scope=Scope.singleton,
    )

    # Register email-related services
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

    # Register Message Broker
    message_broker_config: MessageBrokerConfig = MessageBrokerConfig()
    container.register(
        MessageBrokerConfig,
        instance=message_broker_config,
        scope=Scope.singleton,
    )

    container.register(ConnectionFactory)
    container.register(ChannelFactory)

    container.register(
        BaseMessageBroker,
        RabbitMQMessageBroker,
        scope=Scope.singleton,
    )

    # Register authentication use cases
    container.register(LoginUserInteractor)
    container.register(ValidateTokenInteractor)

    # Register user use cases
    container.register(AddUserInteractor)
    container.register(DeleteUserInteractor)
    container.register(GetUserInteractor)
    container.register(GetAllUserInteractor)

    # Register location use cases
    container.register(AddLocationInteractor)
    container.register(DeleteLocationInteractor)
    container.register(GetLocationInteractor)
    container.register(GetAllLocationInteractor)

    # Register weather use case
    container.register(GetWeatherInteractor)

    return container
