from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get('/')
async def get_all_bookings() -> list[SBooking]:
    result = await BookingDAO.get_all()
    return result


@router.get('/{booking_id:int}')
async def get_all_bookings(booking_id) -> SBooking:
    result = await BookingDAO.get_by_id(booking_id)
    return result


@router.get('/filters')
async def get_all_bookings() -> SBooking:
    result = await BookingDAO.get_one_or_none(room_id=1)
    return result
