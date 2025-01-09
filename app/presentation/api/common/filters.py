from pydantic import BaseModel

from infrastructure.repository.filters import RepositoryFilters


class FiltersSchema(BaseModel):
    offset: int = 0
    limit: int = 10

    def to_repository_filters(self) -> RepositoryFilters:
        return RepositoryFilters(
            offset=self.offset,
            limit=self.limit,
        )
