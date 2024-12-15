from typing import Iterable

from pydantic import BaseModel

from domain.entities.user import User


class GetUserResponseSchema(BaseModel):
    login: str
    password: str

    @classmethod
    def from_entity(cls, user: User) -> "GetUserResponseSchema":
        return cls(login=user.login, password=user.password)


class GetUsersResponseSchema(BaseModel):
    users: Iterable[GetUserResponseSchema]

    @classmethod
    def from_entity(cls, users: Iterable[User]) -> "GetUsersResponseSchema":
        return cls(
            users=[GetUserResponseSchema.from_entity(user) for user in users],
        )


class AddNewUserRequestSchema(BaseModel):
    login: str
    password: str
