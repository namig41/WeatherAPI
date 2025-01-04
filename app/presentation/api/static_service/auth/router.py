from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from presentation.api.static_service.jinja_config import templates


router = APIRouter()


@router.get(
    "/sign-up",
    response_class=HTMLResponse,
)
def sing_up_view(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sign-up.html",
        {"request": request, "key": "value"},
    )


@router.get(
    "/sign-in",
    response_class=HTMLResponse,
)
def sing_in_view(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sign-in.html",
        {"request": request, "key": "value"},
    )
