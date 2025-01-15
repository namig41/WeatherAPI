from dataclasses import dataclass


@dataclass
class UserDTO:
    login: str | None = None
    email: str | None = None
    password: str | None = None
