from datetime import date

from fastapi import APIRouter, Depends

from app.hotels.dao import HotelDAO, RoomDAO
from app.hotels.schemas import SHotel, SRoom, SRoomInfo, SHotelInfo


router = APIRouter(
    prefix="/hotels",
    tags=["Отели и комнаты"]
)


@router.get('/')
async def get_all_by_location(hotel_location: str,
                              date_from: date,
                              date_to: date) -> list[SHotelInfo]:
    result = await HotelDAO.get_all_by_location(hotel_location, date_from, date_to)
    return result


@router.get('/{hotel_id}/rooms')
async def get_all_rooms(hotel_id: int,
                        date_from: date,
                        date_to: date) -> list[SRoomInfo]:
    result = await RoomDAO.get_all_available(hotel_id, date_from, date_to)
    return result


@router.get('/id/{hotel_id}')
async def get_hotel_by_id(hotel_id: int):
    result = await HotelDAO.get_one_or_none(id=hotel_id)
    return result
