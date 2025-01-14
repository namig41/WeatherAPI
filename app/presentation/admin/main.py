from fastapi import FastAPI

import uvicorn
from punq import Container
from sqladmin import Admin
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from bootstrap.di import init_container
from presentation.admin.lifespan import lifespan
from presentation.admin.view.location import LocationAdmin
from presentation.admin.view.user import UserAdmin
from settings.config import config


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        lifespan=lifespan,
        debug=True,
    )

    container: Container = init_container()
    engine: AsyncEngine = container.resolve(AsyncEngine)

    admin: Admin = Admin(app, engine)

    admin.add_view(UserAdmin)
    admin.add_view(LocationAdmin)
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=config.ADMIN_SERVICE_HOST,
        port=config.ADMIN_SERVICE_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
