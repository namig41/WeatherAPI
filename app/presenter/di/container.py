from functools import lru_cache

from infrastructure.auth.access_token_processor import AccessTokenProcessor
from infrastructure.auth.password_hasher import SimplePasswordHasher
from infrastructure.auth.token_access_service import PasswordAuthService
from infrastructure.jwt.base import BaseJWTProcessor
from infrastructure.jwt.jwt_processor import py_jwt_processor_factory
from infrastructure.logger.base import BaseLogger
from infrastructure.logger.logger import create_logger_dependency
from infrastructure.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from infrastructure.repository.memory import (
    MemoryLocationRepository,
    MemoryUserRepository,
)
from punq import (
    Container,
    Scope,
)

from domain.interfaces.infrastructure.access_service import BaseAccessService
from domain.interfaces.infrastructure.password_hasher import BasePasswordHasher


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(
        BaseUserRepository,
        MemoryUserRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseLocationRepository,
        MemoryLocationRepository,
        scope=Scope.singleton,
    )

    container.register(
        BasePasswordHasher,
        SimplePasswordHasher,
        scope=Scope.singleton,
    )

    container.register(
        BaseLogger,
        factory=create_logger_dependency,
        scope=Scope.singleton,
    )

    container.register(
        BaseAccessService,
        PasswordAuthService,
        scope=Scope.singleton,
    )

    container.register(
        BaseJWTProcessor,
        factory=py_jwt_processor_factory,
        scope=Scope.singleton,
    )

    container.register(
        AccessTokenProcessor,
        factory=lambda: AccessTokenProcessor(
            jwt_processor=py_jwt_processor_factory(),
        ),
        scope=Scope.singleton,
    )

    return container
