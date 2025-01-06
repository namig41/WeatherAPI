from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from presentation.api.lifespan import lifespan
from presentation.api.weather_service.location.router import router as location_router
from presentation.api.weather_service.weather.router import router as weather_router
from settings.config import config


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="WeatherAPI",
        docs_url="/api/docs/",
        debug=True,
        lifespan=lifespan,
    )

    origins = [
        "http://localhost:8000",
        "http://localhost",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(location_router)
    app.include_router(weather_router)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=config.WEATHER_SERIVCE_API_HOST,
        port=config.WEATHER_SERIVCE_API_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
