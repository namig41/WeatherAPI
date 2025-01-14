from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from application.auth.auth_decorator import validate_token_decorator
from application.location.dto import LocationDTO
from application.weather.get_weather import GetWeatherInteractor
from bootstrap.di import init_container
from domain.entities.user import User
from domain.entities.weather import Weather
from domain.exceptions.base import ApplicationException
from presentation.api.weather_service.v1.weather.schema import WeatherResponseSchema


router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get(
    "/{location_name}",
    status_code=status.HTTP_200_OK,
    response_model=WeatherResponseSchema,
    description="Получение погоды по имени",
)
@validate_token_decorator
async def get_weather_by_name(
    location_name: str,
    user: User,
    container: Container = Depends(init_container),
) -> WeatherResponseSchema:
    try:
        location_dto: LocationDTO = LocationDTO(
            name=location_name,
            user=user,
        )
        get_weather_action: GetWeatherInteractor = container.resolve(
            GetWeatherInteractor,
        )
        weather: Weather = await get_weather_action(location_dto)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return WeatherResponseSchema.from_entity(weather)
