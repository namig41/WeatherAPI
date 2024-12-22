from email.message import EmailMessage

from infrastructure.email.config import ConfirmationEmailConfig

from domain.entities.location import Location
from domain.entities.user import User
from domain.entities.weather import Weather


def convert_weather_entity_to_message(
    user: User,
    location: Location,
    weather: Weather,
    config: ConfirmationEmailConfig,
) -> EmailMessage:
    message: EmailMessage = EmailMessage()

    message["From"] = config.email_from
    message["To"] = user.email.to_raw()
    message["Subject"] = config.subject

    message.set_content(
        f"Привет, {user.login}!\n\n"
        f"В местоположении {location.name} текущая погода:\n"
        f"- Температура: {weather.temperature}°C\n"
        f"- Описание: {weather.description}\n"
        f"- Влажность: {weather.humidity}%\n"
        f"- Скорость ветра: {weather.wind_speed} м/с\n\n"
        f"Хорошего дня!\n\n"
        f"С уважением, команда {config.email_from.split('@')[1]}",
    )

    return message
