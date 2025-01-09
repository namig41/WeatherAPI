from dataclasses import dataclass


@dataclass
class RepositoryFilters:
    offset: int = 0
    limit: int = 10
