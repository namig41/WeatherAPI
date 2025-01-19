from dataclasses import dataclass
from decimal import Decimal

from domain.entities.user import User
from infrastructure.repository.filters import RepositoryFilters


@dataclass
class LocationDTO:
    name: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    user: User | None = None


@dataclass
class FiltersLocationDTO:
    location: LocationDTO
    filters: RepositoryFilters
