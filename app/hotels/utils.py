from datetime import date

from sqlalchemy import select, and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Booking
from app.hotels.models import Room


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
            or_(
                and_(
                    Booking.date_from >= date_from,
                    Booking.date_from <= date_to,
                ),
                and_(
                    Booking.date_from <= date_from,
                    Booking.date_to > date_from,
                ),
            ),
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


async def get_rooms_left(room_id: int,
                         date_from: date,
                         date_to: date,
                         session: AsyncSession):
    rooms_left = await session.execute(
        query_rooms_left(room_id, date_from, date_to)
    )
    return rooms_left.scalar()
