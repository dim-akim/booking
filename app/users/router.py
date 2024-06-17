from fastapi import APIRouter, HTTPException, status, Response

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.schemas import SUserAuth
from app.users.dao import UserDAO


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    hashed_password = get_password_hash(user_data.password)
    result = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    return result


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token({'sub': user.id})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token