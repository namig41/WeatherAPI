from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import Callable

from jose import jwt
from passlib.context import CryptContext

from application.api.exceptions.user import UserAuthFailedException
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from infra.repository.base import BaseUserRepository
from settings.config import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_plain_password(plain_password: str, password: str) -> bool:
    return plain_password == password


def create_access_token(data: dict, minutes: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode.update({"exp": expire.isoformat()})  # Преобразуем дату в строку
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, config.JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_user(
    login_user: User,
    users_repository: BaseUserRepository,
    verify_password: Callable[[str, str], int],
) -> User:
    try:
        user = await users_repository.get_user_by_login(login=login_user.login)
        if not verify_password(login_user.password, user.password):
            raise UserAuthFailedException()
        return user
    except ApplicationException:
        raise
