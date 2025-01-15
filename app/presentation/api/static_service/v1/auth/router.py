from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
)

from punq import Container

from application.auth.dto import AccessTokenDTO
from application.user.dto import UserDTO
from bootstrap.di import init_container
from domain.exceptions.base import ApplicationException
from infrastructure.auth.access_service_api import AuthServiceAPI
from presentation.api.static_service.v1.jinja_config import templates


router = APIRouter()


@router.post("/sign-in")
async def sign_in(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    redirect_to: str = Form(...),
    container: Container = Depends(init_container),
):
    access_service: AuthServiceAPI = container.resolve(AuthServiceAPI)
    try:
        access_token: AccessTokenDTO = await access_service.login(
            UserDTO(login=username, password=password),
        )
    except ApplicationException as exception:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": exception.message},
        )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "token": access_token.jwt_token},
    )


@router.post("/logout")
async def logout(
    request: Request,
    container: Container = Depends(init_container),
):
    access_service: AuthServiceAPI = container.resolve(AuthServiceAPI)
    try:
        await access_service.logout()
    except ApplicationException as exception:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": exception.message},
        )

    return templates.TemplateResponse(
        "sign-in.html",
        {"request": request},
    )
