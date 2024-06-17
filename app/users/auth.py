from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = 60 * 24 * 30) -> str:
    pass


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.get_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):  # TODO Додумать про обработку неправильного пароля
        return user
