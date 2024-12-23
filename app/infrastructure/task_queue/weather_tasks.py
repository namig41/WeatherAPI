from infrastructure.task_queue.init import celery
from infrastructure.weather.base import IWeatherAPIService

from domain.entities.location import Location
from domain.entities.weather import Weather
from domain.exceptions.base import ApplicationException


@celery.task
async def fetch_weather_from_api(
    weather_api_service: IWeatherAPIService,
    location: Location,
) -> Weather:
    try:
        weather: Weather = await weather_api_service.get_weather_by_location_name(
            location,
        )
        return weather
    except ApplicationException:
        raise
