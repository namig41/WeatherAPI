from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn

from presentation.api.static_service.auth.router import router as auth_view_router
from presentation.api.static_service.root.router import router as main_view_router
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

    app.include_router(main_view_router)
    app.include_router(auth_view_router)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=config.STATIC_SERIVCE_API_HOST,
        port=config.STATIC_SERIVCE_API_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
