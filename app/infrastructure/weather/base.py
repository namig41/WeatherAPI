from abc import abstractmethod
from typing import Protocol

from domain.entities.location import Location
from domain.entities.weather import Weather


class IWeatherAPIService(Protocol):
    @abstractmethod
    async def get_weather_by_location_name(self, location: Location) -> Weather: ...

    @abstractmethod
    async def get_weather_by_location_coordinates(
        self,
        location: Location,
    ) -> Weather: ...
