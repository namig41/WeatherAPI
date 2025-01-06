from pydantic import BaseModel

from domain.entities.user import User


class LoginUserRequestSchema(BaseModel):
    login: str
    password: str


class GetMeResponseSchema(BaseModel):
    user_id: int | None
    login: str
    email: str

    @classmethod
    def from_entity(cls, user: User) -> "GetMeResponseSchema":
        return cls(
            user_id=user.id,
            login=user.login,
            email=user.email.to_raw(),
        )
