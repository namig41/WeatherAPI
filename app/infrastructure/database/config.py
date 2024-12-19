from dataclasses import dataclass

from settings.config import config


@dataclass
class DBConfig:
    DB_USER: str = config.POSTGRES_USER
    DB_PASSWORD: str = config.POSTGRES_PASSWORD
    DB_HOST: str = config.POSTGRES_HOST
    DB_PORT: str = config.POSTGRES_PORT
    DB_NAME: str = config.POSTGRES_DB

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
