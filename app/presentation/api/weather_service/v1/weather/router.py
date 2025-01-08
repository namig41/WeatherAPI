from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

from punq import Container

from application.common.interactor import Interactor
from bootstrap.di import init_container
from domain.entities.weather import Weather
from domain.exceptions.base import ApplicationException
from infrastructure.auth.access_service_api import AuthServiceAPI
from presentation.api.weather_service.v1.weather.schema import WeatherResponseSchema


router = APIRouter(prefix="/weather", tags=["Weather"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get(
    "/{location_name}",
    status_code=status.HTTP_200_OK,
    response_model=WeatherResponseSchema,
    description="Получение погоды по имени",
)
async def get_weather_by_name(
    location_name: str,
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(init_container),
) -> WeatherResponseSchema:
    try:
        auth_service_api: AuthServiceAPI = container.resolve(AuthServiceAPI)
        await auth_service_api.validate_token(token)

        get_weather_action: Interactor[str, Weather] = container.resolve(
            Interactor[str, Weather],
        )
        weather: Weather = await get_weather_action(location_name)

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return WeatherResponseSchema.from_entity(weather)
