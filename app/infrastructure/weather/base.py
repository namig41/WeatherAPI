from abc import abstractmethod
from typing import Protocol

from domain.entities.weather import WeatherData


class IWeatherAPIService(Protocol):
    @abstractmethod
    async def get_weather_by_location(self, location: str) -> WeatherData:
        pass
