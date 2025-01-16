from dataclasses import dataclass

from settings.config import config


@dataclass(frozen=True)
class EventBusConfig:
    host: str = config.MESSAGE_BROKER_HOST
    port: int = config.MESSAGE_BROKER_PORT
    login: str = config.MESSAGE_BROKER_USER
    password: str = config.MESSAGE_BROKER_PASSWORD

    @property
    def get_url(self) -> str:
        return f"amqp://{self.login}:{self.password}@localhost:{self.port}/"
