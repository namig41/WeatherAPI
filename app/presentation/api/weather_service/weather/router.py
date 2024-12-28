from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from bootstrap.di import init_container
from domain.entities.location import Location
from domain.entities.weather import Weather
from domain.exceptions.base import ApplicationException
from infrastructure.cache.base import ICacheWeatherService
from infrastructure.repository.base import BaseLocationRepository
from infrastructure.weather.base import IWeatherAPIService
from presentation.api.weather_service.weather.schema import WeatherResponseSchema


router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get(
    "/{location_name}",
    status_code=status.HTTP_200_OK,
    response_model=WeatherResponseSchema,
    description="Получение погоды по имени",
)
async def get_weather_by_name(
    location_name: str,
    container: Container = Depends(init_container),
) -> WeatherResponseSchema:
    try:
        location_repository: BaseLocationRepository = container.resolve(
            BaseLocationRepository,
        )
        weather_service: IWeatherAPIService = container.resolve(IWeatherAPIService)
        cache_service: ICacheWeatherService = container.resolve(ICacheWeatherService)
        location: Location = await location_repository.get_location_by_name(
            location_name,
        )
        weather: Weather | None = await cache_service.get_weather_by_location_name(
            location,
        )
        if weather is not None:
            return WeatherResponseSchema.from_entity(weather)
        weather = await weather_service.get_weather_by_location_name(location)
        await cache_service.set_weather_by_location_name(location, weather)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return WeatherResponseSchema.from_entity(weather)
