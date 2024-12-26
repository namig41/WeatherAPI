from domain.entities.location import Location
from domain.entities.user import User


def convert_location_entity_to_data(location: Location) -> dict:
    return {
        "name": location.name,
        "latitude": location.latitude,
        "longitude": location.longitude,
    }


def convert_user_entity_to_data(user: User) -> dict:
    return {
        "name": user.login,
        "email": user.email,
        "hashed_password": user.hashed_password.to_raw(),
    }
