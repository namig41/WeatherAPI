from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

from punq import Container

from bootstrap.di import init_container
from domain.entities.location import Location
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infrastructure.auth.access_service_api import AuthServiceAPI
from infrastructure.repository.base import BaseUserLocationRepository
from presentation.api.weather_service.location.schema import (
    AddNewLocationRequestSchema,
    LocationResponseSchema,
    LocationsResponseSchema,
)


router = APIRouter(prefix="/locations", tags=["Location"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=LocationsResponseSchema,
    description="Получение всех локаций",
)
async def get_all_location(
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(init_container),
) -> LocationsResponseSchema:
    try:
        auth_service_api: AuthServiceAPI = container.resolve(AuthServiceAPI)
        user: User = await auth_service_api.validate_token(token)

        location_repository: BaseUserLocationRepository = container.resolve(
            BaseUserLocationRepository,
        )
        locations: Iterable[Location] = await location_repository.get_all_location(user)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return LocationsResponseSchema.from_entity(locations)


@router.get(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=LocationResponseSchema,
    description="Получение локации по имени",
)
async def get_location(
    name: str,
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(init_container),
) -> LocationResponseSchema:
    try:
        auth_service_api: AuthServiceAPI = container.resolve(AuthServiceAPI)
        user: User = await auth_service_api.validate_token(token)

        location_repository: BaseUserLocationRepository = container.resolve(
            BaseUserLocationRepository,
        )
        location: Location = await location_repository.get_location_by_name(
            user,
            name=name,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return LocationResponseSchema.from_entity(location)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationResponseSchema,
    description="Добавление новой локации",
)
async def add_location(
    location_data: AddNewLocationRequestSchema,
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(init_container),
) -> LocationResponseSchema:
    try:
        auth_service_api: AuthServiceAPI = container.resolve(AuthServiceAPI)
        user: User = await auth_service_api.validate_token(token)

        location_repository: BaseUserLocationRepository = container.resolve(
            BaseUserLocationRepository,
        )
        location: Location = Location(
            location_data.name,
            location_data.latitude,
            location_data.longitude,
        )
        await location_repository.add_location(user, location)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return LocationResponseSchema.from_entity(location)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Добавление новой локации",
)
async def delete_location(
    location_name: str,
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(init_container),
) -> None:
    try:
        auth_service_api: AuthServiceAPI = container.resolve(AuthServiceAPI)
        user: User = await auth_service_api.validate_token(token)

        location_repository: BaseUserLocationRepository = container.resolve(
            BaseUserLocationRepository,
        )
        await location_repository.delete_location_by_name(user=user, name=location_name)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
