from datetime import date

from fastapi import APIRouter, Depends

from app.exceptions import RoomCanNotBeBookedException, BookingCannotBeDeletedException
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import User


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get('')
async def get_all_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.get_all_with_images(user.id)
    return result


@router.post('/add', status_code=201)
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


@router.delete('/{booking_id}', status_code=204)
async def delete_booking(booking_id: int, user: User = Depends(get_current_user)):
    booking = await BookingDAO.delete(id=booking_id, user_id=user.id)
    if not booking:
        raise BookingCannotBeDeletedException()
