from dataclasses import dataclass
from typing import Iterable

from application.common.interactor import Interactor
from domain.entities.user import User
from infrastructure.repository.base import BaseUserRepository
from infrastructure.repository.filters import RepositoryFilters


@dataclass
class GetAllUserInteractor(Interactor[RepositoryFilters, Iterable[User]]):
    users_repository: BaseUserRepository

    async def __call__(self, filters: RepositoryFilters) -> Iterable[User]:
        users: Iterable[User] = await self.users_repository.get_all_user(filters)
        return users
