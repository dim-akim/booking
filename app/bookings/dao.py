from app.bookings.models import Booking
from app.dao import BaseDAO


class BookingDAO(BaseDAO):
    model = Booking
