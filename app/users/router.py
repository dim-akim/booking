from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import SUserAuth
from app.users.dao import UserDAO
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException()
    hashed_password = get_password_hash(user_data.password)
    result = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    return result


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException()
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("booking_access_token")
    return {'status': 'success', 'message': ''}


@router.get('/me')
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
