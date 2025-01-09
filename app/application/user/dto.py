from dataclasses import dataclass


@dataclass
class UserDataDTO:
    login: str
    email: str
    password: str
