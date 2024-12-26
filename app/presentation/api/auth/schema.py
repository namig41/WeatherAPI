from pydantic import BaseModel

from domain.entities.user import User


class LoginUserRequestSchema(BaseModel):
    login: str
    password: str


class GetMeResponseSchema(BaseModel):
    login: str
    email: str
    password: str

    @classmethod
    def from_entity(cls, user: User) -> "GetMeResponseSchema":
        return cls(
            login=user.login,
            email=user.email.to_raw(),
            password=user.hashed_password.to_raw(),
        )
