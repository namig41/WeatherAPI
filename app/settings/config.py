from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str
    API_PORT: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str


config = Settings()