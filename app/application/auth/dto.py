from dataclasses import dataclass

from infrastructure.jwt.access_token import JWTToken


@dataclass
class AccessTokenDTO:
    access_token: JWTToken
    token_type: str
