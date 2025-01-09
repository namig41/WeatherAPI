from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str

    AUTH_SERVICE_API_HOST: str
    AUTH_SERVICE_API_PORT: int

    WEATHER_SERVICE_API_HOST: str
    WEATHER_SERVICE_API_PORT: int

    STATIC_SERVICE_API_HOST: str
    STATIC_SERVICE_API_PORT: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_TEST_DB: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    WEATHER_API_KEY: str
    WEATHER_API_URL: str

    CACHE_HOST: str
    CACHE_PORT: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str


config: Settings = Settings()
