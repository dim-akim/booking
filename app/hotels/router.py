from datetime import date

from fastapi import APIRouter, Depends

from app.exceptions import RoomCanNotBeBookedException
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import User


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get('/')
async def get_all_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.get_all(user_id=user.id)
    return result


@router.get('/{booking_id:int}')
async def get_all_bookings(booking_id) -> SBooking:
    result = await BookingDAO.get_one_or_none(id=booking_id)
    return result


@router.get('/filters')
async def get_all_bookings() -> SBooking:
    result = await BookingDAO.get_one_or_none(room_id=1)
    return result


@router.post('/add')
async def add_booking(room_id: int, date_from: date, date_to: date,
                      user: User = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBookedException()
    return {
        'status': 'success',
        'message': {
            'booking': booking,
        }
    }
