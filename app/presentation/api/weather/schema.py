from pydantic import BaseModel

from domain.entities.weather import Weather


class WeatherResponseSchema(BaseModel):
    temperature: float
    description: str
    wind_speed: float
    humidity: int

    @classmethod
    def from_entity(cls, weather_data: Weather) -> "WeatherResponseSchema":
        return cls(
            temperature=weather_data.temperature,
            description=weather_data.description,
            wind_speed=weather_data.wind_speed,
            humidity=weather_data.humidity,
        )
