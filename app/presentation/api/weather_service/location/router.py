from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from bootstrap.di import init_container
from domain.entities.location import Location
from domain.exceptions.base import ApplicationException
from infrastructure.repository.base import BaseLocationRepository
from presentation.api.weather_service.location.schema import (
    AddNewLocationRequestSchema,
    LocationResponseSchema,
    LocationsResponseSchema,
)


router = APIRouter(prefix="/locations", tags=["Location"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=LocationsResponseSchema,
    description="Получение всех локаций",
)
async def get_all_location(
    container: Container = Depends(init_container),
) -> LocationsResponseSchema:
    try:
        location_repository: BaseLocationRepository = container.resolve(
            BaseLocationRepository,
        )
        locations: Iterable[Location] = await location_repository.get_all_location()
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
    container: Container = Depends(init_container),
) -> LocationResponseSchema:
    try:
        location_repository: BaseLocationRepository = container.resolve(
            BaseLocationRepository,
        )
        location: Location = await location_repository.get_location_by_name(
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
    container: Container = Depends(init_container),
) -> LocationResponseSchema:
    try:
        location_repository: BaseLocationRepository = container.resolve(
            BaseLocationRepository,
        )
        location: Location = Location(
            location_data.name,
            location_data.latitude,
            location_data.longitude,
        )
        await location_repository.add_location(location)
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
    container: Container = Depends(init_container),
) -> None:
    try:
        location_repository: BaseLocationRepository = container.resolve(
            BaseLocationRepository,
        )
        await location_repository.delete_location_by_name(name=location_name)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
