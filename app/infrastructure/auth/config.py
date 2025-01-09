from dataclasses import dataclass

from settings.config import config


@dataclass
class AuthConfig:
    host: str = config.AUTH_SERVICE_API_HOST
    port: int = config.AUTH_SERVICE_API_PORT

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"
