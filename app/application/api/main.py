from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from infrastructure.database.models import create_database
from sqlalchemy import Engine

from application.api.auth.router import router as auth_router
from application.api.location.router import router as location_router
from application.api.user.router import router as user_router
from application.di.container import init_container


def create_app() -> FastAPI:
    app = FastAPI(title="WeatherAPI", docs_url="/api/docs/", debug=True)

    app.include_router(location_router)
    app.include_router(user_router)
    app.include_router(auth_router)

    origins = ["http://localhost:8000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    container = init_container()

    engine: Engine = container.resolve(Engine)
    create_database(engine)

    uvicorn.run(
        "main:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
        workers=1,
    )
