from abc import abstractmethod
from typing import Protocol

from domain.entities.location import Location
from domain.entities.weather import Weather


class ICacheWeatherService(Protocol):

    @abstractmethod
    async def get_weather_by_location_name(
        self, location: Location,
    ) -> Weather | None: ...

    @abstractmethod
    async def set_weather_by_location_name(
        self, location: Location, weather: Weather,
    ) -> None: ...
