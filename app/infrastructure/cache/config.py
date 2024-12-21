from dataclasses import dataclass

from settings.config import config


@dataclass
class CacheConfig:
    host: str = config.CACHE_HOST
    port: str = config.CACHE_PORT

    def get_url(self, schema: str) -> str:
        return f"{schema}://{self.host}:{self.port}"
