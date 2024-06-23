from datetime import date

from fastapi import APIRouter, Depends

from app.exceptions import RoomCanNotBeBookedException
from app.hotels.dao import HotelDAO, RoomDAO
from app.hotels.schemas import SHotel, SRoom, SRoomInfo, SHotelInfo
from app.users.dependencies import get_current_user
from app.users.models import User


router = APIRouter(
    prefix="/hotels",
    tags=["Отели и комнаты"]
)


@router.get('/{hotel_id}/rooms')
async def get_all_rooms(hotel_id: int,
                        date_from: date,
                        date_to: date) -> list[SRoomInfo]:
    result = await RoomDAO.get_all_available(hotel_id, date_from, date_to)
    return result


@router.get('/{hotel_location}')
async def get_all_rooms(hotel_location: str,
                        date_from: date,
                        date_to: date) -> list[SHotelInfo]:
    result = await HotelDAO.get_all()
    return result


# @router.get('/{booking_id:int}')
# async def get_all_bookings(booking_id) -> SBooking:
#     result = await BookingDAO.get_one_or_none(id=booking_id)
#     return result
#
#
# @router.get('/filters')
# async def get_all_bookings() -> SBooking:
#     result = await BookingDAO.get_one_or_none(room_id=1)
#     return result
#
#
# @router.post('/add')
# async def add_booking(room_id: int, date_from: date, date_to: date,
#                       user: User = Depends(get_current_user)):
#     booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
#     if not booking:
#         raise RoomCanNotBeBookedException()
#     return {
#         'status': 'success',
#         'message': {
#             'booking': booking,
#         }
#     }
