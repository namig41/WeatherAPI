from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from infra.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from infra.repository.memory import (
    MemoryLocationRepository,
    MemoryUserRepository,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(BaseUserRepository, MemoryUserRepository, scope=Scope.singleton)
    container.register(
        BaseLocationRepository,
        MemoryLocationRepository,
        scope=Scope.singleton,
    )

    return container
