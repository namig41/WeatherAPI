from dataclasses import dataclass

from httpx import (
    AsyncClient,
    HTTPStatusError,
    Response,
)
from infrastructure.exceptions.weather import WeatherAPIServiceException
from infrastructure.weather.base import IWeatherAPIService
from infrastructure.weather.config import WeatherAPIConfig
from infrastructure.weather.converters import convert_weather_data_to_entity

from domain.entities.location import Location
from domain.entities.weather import Weather


@dataclass
class OpenWeatherAPIService(IWeatherAPIService):
    weather_api_config: WeatherAPIConfig

    async def get_weather_by_location_name(self, location: Location) -> Weather:
        async with AsyncClient() as client:
            try:
                response: Response = await client.get(
                    f"{self.weather_api_config.base_url}/weather",
                    params={
                        "q": location.name,
                        "appid": self.weather_api_config.api_key,
                        "units": "metric",
                    },
                )
                response.raise_for_status()
                weather_data: dict = response.json()

                return convert_weather_data_to_entity(weather_data)
            except HTTPStatusError:
                raise WeatherAPIServiceException()

    async def get_weather_by_location_coordinates(self, location: Location) -> Weather:
        try:
            async with AsyncClient() as client:
                response: Response = await client.get(
                    f"{self.weather_api_config.base_url}/weather",
                    params={
                        "lat": float(location.latitude),
                        "lon": float(location.longitude),
                        "appid": self.weather_api_config.api_key,
                        "units": "metric",
                    },
                )
                response.raise_for_status()
                weather_data: dict = response.json()

                return convert_weather_data_to_entity(weather_data)
        except HTTPStatusError:
            raise WeatherAPIServiceException()
