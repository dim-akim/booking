from datetime import date

from sqlalchemy import select, and_, func, or_, insert

from app.bookings.models import Booking
from app.dao import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Room
from app.hotels.dao import dates_within_range


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def get_all_with_images(cls,
                                  user_id: int):
        query_get_bookings = (
            select(
                Booking.__table__.columns,
                Room.__table__.columns
            )
            .select_from(Booking)
            .outerjoin(Room, Booking.room_id == Room.id)
            .where(Booking.user_id == user_id)
        )

        async with async_session_maker() as session:
            bookings = await session.execute(query_get_bookings)
            return bookings

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date):
        async with async_session_maker() as session:
            rooms_left = await session.execute(
                query_rooms_left(room_id, date_from, date_to)
            )
            rooms_left = rooms_left.scalar()

            if rooms_left:
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


def query_booked_rooms(room_id: int,
                       date_from: date,
                       date_to: date):
    """
    WITH booked_rooms AS (
    SELECT * FROM bookings
    WHERE room_id = 1 AND
    date_from >= '2023-05-15' AND date_from <= '2023-06-20' OR
    date_from <= '2023-05-15' AND date_to > '2023-05-15'
    )
    """
    return select(Booking).where(
        and_(
            Booking.room_id == room_id,
            dates_within_range(date_from, date_to)
        )
    ).cte('booked_rooms')


def query_rooms_left(room_id: int,
                     date_from: date,
                     date_to: date):
    """
    SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
    LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
    WHERE rooms.id = 1
    GROUP BY rooms.quantity, booked_rooms.room_id
    """

    booked_rooms = query_booked_rooms(room_id, date_from, date_to)

    return select(
        (Room.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
    ).select_from(Room).outerjoin(
        booked_rooms, booked_rooms.c.room_id == Room.id
    ).where(Room.id == room_id).group_by(Room.id, booked_rooms.c.room_id)
