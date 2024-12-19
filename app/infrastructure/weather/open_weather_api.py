from dataclasses import dataclass

from httpx import (
    AsyncClient,
    Response,
)
from infrastructure.weather.base import IWeatherAPIService
from infrastructure.weather.converters import convert_weather_data_to_entity

from domain.entities.weather import WeatherData


@dataclass
class OpenWeatherService(IWeatherAPIService):
    api_key: str
    base_url: str = "https://api.openweathermap.org/data/2.5"

    async def get_weather_by_location(self, location: str) -> WeatherData:
        async with AsyncClient() as client:
            response: Response = await client.get(
                f"{self.base_url}/weather",
                params={"q": location, "appid": self.api_key, "units": "metric"},
            )
            response.raise_for_status()
            data = response.json()

            return convert_weather_data_to_entity(data)
