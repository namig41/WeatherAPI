from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str
    API_PORT: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


config = Settings()
