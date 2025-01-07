from dataclasses import dataclass

from fastapi import APIRouter, status

router = APIRouter(
    prefix="/ping",
    tags=["Ping"],
)


@dataclass(frozen=True)
class OkStatus:
    status: str = "OK"


OK_STATUS = OkStatus()


@router.get("", status_code=status.HTTP_200_OK)
async def get_status() -> OkStatus:
    return OK_STATUS