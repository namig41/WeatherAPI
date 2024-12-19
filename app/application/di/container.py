from functools import (
    lru_cache,
    partial,
)

from infrastructure.auth.access_service import PasswordAuthService
from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.auth.password_hasher import SimplePasswordHasher
from infrastructure.database.config import DBConfig
from infrastructure.database.init import init_database
from infrastructure.jwt.base import BaseJWTProcessor
from infrastructure.jwt.config import JWTConfig
from infrastructure.jwt.jwt_processor import PyJWTProcessor
from infrastructure.logger.base import ILogger
from infrastructure.logger.logger import create_logger_dependency
from infrastructure.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from infrastructure.repository.postgres import (
    PostgreSQLLocationRepository,
    PostgreSQLUserRepository,
)
from punq import (
    Container,
    Scope,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from domain.interfaces.infrastructure.access_service import IAccessService
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from settings.config import (
    config,
    Settings,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(
        Settings,
        instance=config,
        scope=Scope.singleton,
    )

    jwt_config: JWTConfig = JWTConfig(
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM,
    )

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

    db_config: DBConfig = DBConfig()

    container.register(
        DBConfig,
        isinstance=db_config,
        scope=Scope.singleton,
    )

    container.register(
        AsyncEngine,
        factory=partial(init_database, db_config=db_config),
        scope=Scope.singleton,
    )

    container.register(
        BaseUserRepository,
        PostgreSQLUserRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseLocationRepository,
        PostgreSQLLocationRepository,
        scope=Scope.singleton,
    )

    container.register(
        IPasswordHasher,
        SimplePasswordHasher,
        scope=Scope.singleton,
    )

    container.register(
        IAccessService,
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

    return container
