from enum import Enum

from infrastructure.email.config import ConfirmationEmailConfig


class EmailMessageType(Enum):
    REGISTRATION = "registration"
    AUTHORIZATION = "authorization"


class ConfirmationEmailConfigFactory:
    @staticmethod
    def create(message_type: EmailMessageType) -> ConfirmationEmailConfig:
        if message_type == EmailMessageType.REGISTRATION:
            return ConfirmationEmailConfig(
                email_from="namigguseynov@yandex.ru",
                subject="Добро пожаловать на наш сервис!",
                company_name="WeatherAPI",
            )
        elif message_type == EmailMessageType.AUTHORIZATION:
            return ConfirmationEmailConfig(
                email_from="namigguseynov@yandex.ru",
                subject="Авторизация пользователя",
                company_name="WeatherAPI",
            )
        else:
            raise ValueError(f"Unknown message type: {message_type}")
