from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from punq import Container

from bootstrap.di import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infrastructure.auth.access_service_api import AuthServiceAPI
from presentation.api.static_service.v1.jinja_config import templates


router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    description="Главная страница",
)
async def index_view(
    request: Request,
    container: Container = Depends(init_container),
) -> HTMLResponse:
    token = request.headers.get("Authorization")

    if token is None:
        return RedirectResponse(url="/sign-in")

    access_service: AuthServiceAPI = container.resolve(AuthServiceAPI)
    try:
        user: User = await access_service.validate_token(token)
    except ApplicationException:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "key": "value"},
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "key": "value",
            "name": user.login,
        },
    )
