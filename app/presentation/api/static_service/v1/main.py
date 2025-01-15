from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

from presentation.api.static_service.v1.auth.router import router as auth_router
from presentation.api.static_service.v1.auth.view import router as auth_view_router
from presentation.api.static_service.v1.healthcheck import router as healthcheck_router
from presentation.api.static_service.v1.root.router import router as main_view_router
from settings.config import config


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="StaticServiceAPI",
        docs_url="/api/docs/",
        description="Сервис для получения статического контента",
        debug=True,
    )

    static_directory = Path(__file__).parent / "templates"
    app.mount("/static", StaticFiles(directory=static_directory), name="static")

    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(healthcheck_router)
    app.include_router(main_view_router)

    app.include_router(auth_view_router)
    app.include_router(auth_router)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=config.STATIC_SERVICE_API_HOST,
        port=config.STATIC_SERVICE_API_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
