from dataclasses import dataclass
from enum import (
    auto,
    Enum,
)

from infrastructure.email.config import (
    ConfirmationEmailConfig,
    SMTPConfig,
)


class EmailMessageType(Enum):
    REGISTRATION = auto()
    AUTHORIZATION = auto()


@dataclass
class ConfirmationEmailConfigFactory:

    config: SMTPConfig

    def create(self, message_type: EmailMessageType) -> ConfirmationEmailConfig:
        if message_type == EmailMessageType.REGISTRATION:
            return ConfirmationEmailConfig(
                email_from=self.config.username,
                subject="Добро пожаловать на наш сервис!",
                company_name="WeatherAPI",
            )
        elif message_type == EmailMessageType.AUTHORIZATION:
            return ConfirmationEmailConfig(
                email_from=self.config.username,
                subject="Авторизация пользователя",
                company_name="WeatherAPI",
            )
