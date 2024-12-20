from dataclasses import dataclass

from settings.config import config


@dataclass
class CacheConfig:
    host: str = config.CACHE_HOST
    port: str = config.CACHE_PORT

    def get_url(self, service_name: str) -> str:
        return f"{service_name}://{self.host}:{self.port}"
