from sqlalchemy.ext.declarative import as_declarative

from infrastructure.database.models import (
    locations,
    users,
)


@as_declarative()
class AdminBase:
    pass


class UserProxy(AdminBase):
    __table__ = users  # Привязка к вашей таблице


class LocationProxy(AdminBase):
    __table__ = locations  # Привязка к вашей таблице
