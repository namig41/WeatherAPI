from dataclasses import dataclass


@dataclass
class User:
    id: int | None = None


user = User()
