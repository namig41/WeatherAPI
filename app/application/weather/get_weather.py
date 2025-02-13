from dataclasses import dataclass

from application.common.interactor import Interactor
from application.location.dto import LocationDTO
from domain.entities.location import Location
from domain.entities.weather import Weather
from infrastructure.cache.base import ICacheWeatherService
from infrastructure.repository.base import BaseUserLocationRepository
from infrastructure.weather.base import IWeatherAPIService


@dataclass
class GetWeatherInteractor(Interactor[LocationDTO, Weather]):
    weather_service: IWeatherAPIService
    cache_service: ICacheWeatherService
    location_repository: BaseUserLocationRepository

    async def __call__(self, location_dto: LocationDTO) -> Weather:
        location: Location = await self.location_repository.get_location_by_name(
            user=location_dto.user,
            name=location_dto.name,
        )
        weather: Weather | None = await self.cache_service.get_weather_by_location_name(
            location,
        )
        if weather is not None:
            return weather

        weather = await self.weather_service.get_weather_by_location_name(location)
        await self.cache_service.set_weather_by_location_name(location, weather)

        return weather
