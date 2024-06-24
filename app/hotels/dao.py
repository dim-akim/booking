from datetime import date, timedelta

from sqlalchemy import select, and_, func, or_, insert

from app.hotels.models import Hotel, Room
from app.bookings.models import Booking
from app.dao import BaseDAO
from app.database import async_session_maker, engine


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def get_all_by_location(cls,
                                  location: str,
                                  date_from: date,
                                  date_to: date):
        """
        SELECT hotel_id, SUM(quantity - COALESCE(booked, 0)) AS rooms_left
        FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = id
        GROUP BY hotel_id

        SELECT hotel_id, name, location, rooms_left
        FROM hotels
        LEFT JOIN booked_hotels ON id = booked_hotels.hotel_id
        WHERE location LIKE '%Алтай%' AND rooms_left > 10
        """

        booked_rooms = query_booked_rooms(date_from, date_to)

        booked_hotels = (
            select(
                Room.hotel_id,
                func.sum(Room.quantity - func.coalesce(booked_rooms.c.booked, 0)).label('rooms_left')
            )
            .select_from(Room)
            .outerjoin(booked_rooms, Room.id == booked_rooms.c.room_id)
            .group_by(Room.hotel_id)
            .cte('booked_hotels')
        )

        query_get_hotels = (
            select(
                Hotel.__table__.columns,
                booked_hotels.c.rooms_left
            )
            .select_from(Hotel)
            .outerjoin(booked_hotels, Hotel.id == booked_hotels.c.hotel_id)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotel.location.like(f'%{location}%')
                )
            )
        )

        async with async_session_maker() as session:
            hotels = await session.execute(query_get_hotels)
            return hotels.mappings().all()


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def get_all_available(cls,
                                hotel_id: int,
                                date_from: date,
                                date_to: date):

        booked_rooms = (
            select(
                Booking.room_id, func.count(Booking.room_id).label('booked')
            )
            .select_from(Booking)
            .where(dates_within_range(date_from, date_to))
            .group_by(Booking.room_id)
            .cte('booked_rooms')
        )

        query_get_rooms = (
            select(
                Room.__table__.columns,
                (Room.price * (date_to - date_from).days).label('total_cost'),
                (Room.quantity - func.coalesce(booked_rooms.c.booked, 0)).label('rooms_left')
            )
            .select_from(Room).outerjoin(booked_rooms, Room.id == booked_rooms.c.room_id)
            .where(Room.hotel_id == hotel_id)
            .group_by(Room.id, booked_rooms.c.booked)
        )

        async with async_session_maker() as session:
            hotel_rooms = await session.execute(query_get_rooms)
            return hotel_rooms.mappings().all()


def dates_within_range(date_from, date_to):
    """
    date_from >= '2023-06-15' AND date_from <= '2023-06-30' OR
    date_from <= '2023-06-15' AND date_to > '2023-06-15'
    """
    return or_(
                and_(
                    Booking.date_from >= date_from,
                    Booking.date_from <= date_to,
                ),
                and_(
                    Booking.date_from <= date_from,
                    Booking.date_to > date_from,
                ),
            )


def query_booked_rooms(date_from, date_to):
    """
    WITH booked_rooms AS (
       SELECT room_id, COUNT(room_id) as booked
       FROM bookings
       WHERE date_from >= '2023-06-15' AND date_from <= '2023-06-30' OR
       date_from <= '2023-06-15' AND date_to > '2023-06-15'
       GROUP BY room_id
    )
    """
    return (
        select(
            Booking.room_id, func.count(Booking.room_id).label('booked')
        )
        .select_from(Booking)
        .where(dates_within_range(date_from, date_to))
        .group_by(Booking.room_id)
        .cte('booked_rooms')
    )
