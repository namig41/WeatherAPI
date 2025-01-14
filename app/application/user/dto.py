from dataclasses import dataclass


@dataclass
class UserDataDTO:
    login: str | None = None
    email: str | None = None
    password: str | None = None
