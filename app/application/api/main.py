from fastapi import FastAPI

import uvicorn

from application.api.location.router import router as location_router


def create_app() -> FastAPI:
    app = FastAPI(title="WeatherAPI", docs_url="/api/docs/", debug=True)

    app.include_router(location_router)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
        workers=1,
    )
