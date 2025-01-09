from decimal import Decimal

from faker import Faker

from domain.entities.location import Location


def test_location_entity(faker: Faker) -> None:
    name: str = faker.city()
    latitude: Decimal = faker.latitude()
    longitude: Decimal = faker.longitude()
    location: Location = Location(
        name,
        latitude,
        longitude,
    )

    assert location.name == name
    assert location.latitude == latitude
    assert location.longitude == longitude
