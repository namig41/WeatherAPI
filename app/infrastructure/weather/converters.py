from domain.entities.weather import WeatherData


def convert_weather_data_to_entity(weather_data: dict) -> WeatherData:
    return WeatherData(
        temperature=weather_data["main"]["temp"],
        description=weather_data["weather"][0]["description"],
        wind_speed=weather_data["wind"]["speed"],
        humidity=weather_data["main"]["humidity"],
    )
