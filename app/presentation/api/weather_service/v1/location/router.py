from typing import Iterable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from application.auth.auth_decorator import validate_token_decorator
from application.location.add_location import AddLocationInteractor
from application.location.delete_location import DeleteLocationInteractor
from application.location.dto import (
    FiltersLocationDTO,
    LocationDTO,
)
from application.location.get_all_location import GetAllLocationInteractor
from application.location.get_location import GetLocationInteractor
from bootstrap.di import init_container
from domain.entities.location import Location
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from presentation.api.common.filters import FiltersSchema
from presentation.api.weather_service.v1.location.schema import (
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
@validate_token_decorator
async def get_all_location(
    user: User,
    filters_schema: FiltersSchema = Depends(),
    container: Container = Depends(init_container),
) -> LocationsResponseSchema:
    try:
        get_all_location_action: GetAllLocationInteractor = container.resolve(
            GetAllLocationInteractor,
        )

        filter_location_dto: FiltersLocationDTO = FiltersLocationDTO(
            location=LocationDTO(user=user),
            filters=filters_schema.to_repository_filters(),
        )

        locations: Iterable[Location] = await get_all_location_action(
            filter_location_dto,
        )
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
@validate_token_decorator
async def get_location(
    name: str,
    user: User,
    container: Container = Depends(init_container),
) -> LocationResponseSchema:
    try:
        location_dto: LocationDTO = LocationDTO(
            name=name,
            user=user,
        )

        get_location_action: GetLocationInteractor = container.resolve(
            GetLocationInteractor,
        )
        location: Location = await get_location_action(location_dto)
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
@validate_token_decorator
async def add_location(
    location_data: AddNewLocationRequestSchema,
    user: User,
    container: Container = Depends(init_container),
) -> LocationResponseSchema:
    try:
        location_dto: LocationDTO = LocationDTO(
            name=location_data.name,
            latitude=location_data.latitude,
            longitude=location_data.latitude,
            user=user,
        )

        add_location_action: AddLocationInteractor = container.resolve(
            AddLocationInteractor,
        )
        location: Location = await add_location_action(location_dto)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return LocationResponseSchema.from_entity(location)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление локации",
)
@validate_token_decorator
async def delete_location(
    location_name: str,
    user: User,
    container: Container = Depends(init_container),
) -> None:
    try:
        location_dto: LocationDTO = LocationDTO(
            name=location_name,
            user=user,
        )

        delete_location_action: AddLocationInteractor = container.resolve(
            DeleteLocationInteractor,
        )
        await delete_location_action(location_dto)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
