from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.bookings.router import router as booking_router
from app.users.router import router as users_router
from app.hotels.router import router as hotel_router


app = FastAPI()

app.include_router(users_router)
app.include_router(booking_router)
app.include_router(hotel_router)


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


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


# @app.get('/hotels')
# def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotel]:
#     hotels = [
#         {
#             'address': 'ул. Ленина, 1',
#             'name': '1st Hotel',
#             'stars': 5
#         }
#     ]
#     return hotels
