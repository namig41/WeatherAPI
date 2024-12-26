from domain.entities.user import User


def convert_location_data_to_entity(location_data: dict) -> User:
    return User(
        name=location_data["name"],
        latitude=location_data["latitude"],
        longitude=location_data["longitude"],
    )
