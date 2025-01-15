from sqlalchemy.ext.declarative import as_declarative

from infrastructure.database.models import (
    locations,
    users,
)


@as_declarative()
class AdminBase:
    pass


class UserProxy(AdminBase):
    __table__ = users


class LocationProxy(AdminBase):
    __table__ = locations
