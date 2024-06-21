from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenAbsentException, IncorrectTokenFormatException
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException()
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException()
    expire: str = payload.get("exp")
    if not expire:
        raise IncorrectTokenFormatException()
    if int(expire) < datetime.utcnow().timestamp():
        raise IncorrectTokenFormatException()

    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectTokenFormatException()

    user = await UserDAO.get_one_or_none(id=int(user_id))
    if not user:
        raise IncorrectTokenFormatException()

    return user
