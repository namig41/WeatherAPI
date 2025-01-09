from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from presentation.api.auth_service.v1.auth.router import router as auth_router
from presentation.api.auth_service.v1.healthcheck import router as healthcheck_router
from presentation.api.auth_service.v1.user.router import router as user_router
from presentation.api.lifespan import lifespan
from settings.config import config


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="AuthService WeatherAPI",
        docs_url="/api/docs/",
        debug=True,
        lifespan=lifespan,
    )

    origins = [
        "*",
        "http://myapi.local",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(healthcheck_router)
    app.include_router(user_router)
    app.include_router(auth_router)

    return app


if __name__ == "__main__":

    uvicorn.run(
        "main:create_app",
        factory=True,
        host=config.AUTH_SERVICE_API_HOST,
        port=config.AUTH_SERVICE_API_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
