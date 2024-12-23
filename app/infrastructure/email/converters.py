from email.message import EmailMessage

from infrastructure.email.config import SMTPConfig

from domain.entities.location import Location
from domain.entities.user import User
from domain.entities.weather import Weather


def convert_recieve_weather_to_email_message(
    user: User,
    location: Location,
    weather: Weather,
    config: SMTPConfig,
) -> EmailMessage:
    message: EmailMessage = EmailMessage()

    message["From"] = config.username
    message["To"] = user.email.to_raw()
    message["Subject"] = "Прогноз погоды"

    message.set_content(
        f"Привет, {user.login}!\n\n"
        f"В местоположении {location.name} текущая погода:\n"
        f"- Температура: {weather.temperature}°C\n"
        f"- Описание: {weather.description}\n"
        f"- Влажность: {weather.humidity}%\n"
        f"- Скорость ветра: {weather.wind_speed} м/с\n\n"
        f"Хорошего дня!\n\n"
        f"С уважением, команда {config.username.split('@')[1]}",
    )

    return message


def convert_user_register_to_email_message(
    user: User,
    config: SMTPConfig,
) -> EmailMessage:
    message: EmailMessage = EmailMessage()

    message["From"] = config.username
    message["To"] = user.email.to_raw()
    message["Subject"] = "Регистрация пользователя"

    message.set_content(
        f"Здравствуйте, {user.login}!\n\n"
        f"Благодарим вас за регистрацию на нашем сервисе. Ваш аккаунт был успешно создан.\n\n"
        f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нашей службой поддержки.\n\n"
        f"С уважением, команда {config.username.split('@')[1]}",
    )

    return message


def convert_user_auth_to_email_message(
    user: User,
    config: SMTPConfig,
) -> EmailMessage:
    message: EmailMessage = EmailMessage()

    message["From"] = config.username
    message["To"] = user.email.to_raw()
    message["Subject"] = "Уведомление о входе в аккаунт"

    message.set_content(
        f"Здравствуйте, {user.login}!\n\n"
        f"Мы зафиксировали вход в ваш аккаунт. Если это были вы, ничего делать не нужно.\n"
        f"Если вы не выполняли вход, рекомендуем немедленно сменить пароль и связаться с нашей службой поддержки.\n\n"
        f"С уважением, команда {config.username.split('@')[1]}",
    )

    return message
