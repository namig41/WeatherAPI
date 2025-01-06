from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from presentation.api.static_service.v1.jinja_config import templates


router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
)
def index_view(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "key": "value"},
    )
