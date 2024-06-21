from datetime import date

from sqlalchemy import select, and_, func, or_, insert

from app.hotels.models import Hotel, Room
from app.bookings.models import Booking
from app.dao import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.utils import get_rooms_left


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date):

        async with async_session_maker() as session:
            rooms_left = await get_rooms_left(room_id, date_from, date_to, session)

            if rooms_left > 0:
                query_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(query_price)
                price = price.scalar()
                query_add_booking = insert(Booking).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Booking)

                new_booking = await session.execute(query_add_booking)
                await session.commit()
                return new_booking.scalar()


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def get_all_available(cls,
                                hotel_id: int,
                                date_from: date,
                                date_to: date):
        pass
