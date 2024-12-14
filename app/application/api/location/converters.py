from domain.entities.location import Location


def convert_location_data_to_entity(location_data: dict) -> Location:
    return Location(
        name=location_data["name"],
        latitude=location_data["latitude"],
        longitude=location_data["longitude"],
    )
