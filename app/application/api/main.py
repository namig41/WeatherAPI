from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="WeatherAPI", docs_url="/api/docs/", debug=True)

    return app
