from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date


app = FastAPI()


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            stars: Optional[int] = Query(None, ge=1, le=5),
            has_spa: Optional[bool] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get('/hotels')
def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotel]:
    hotels = [
        {
            'address': 'ул. Ленина, 1',
            'name': '1st Hotel',
            'stars': 5
        }
    ]
    return hotels


@app.post('/bookings')
def add_booking(booking: SBooking):
    pass
