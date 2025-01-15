from dataclasses import dataclass

from infrastructure.jwt.access_token import JWTToken


@dataclass
class AccessTokenDTO:
    jwt_token: JWTToken
    type: str = "Bearer"
