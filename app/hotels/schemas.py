from datetime import date

from pydantic import BaseModel

# Для объединения моделей Pydantic и объектов SQLAlchemy есть библиотека SQLModel, чтобы не нарушать DRY


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class SHotelInfo(SHotel):
    rooms_left: int


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int
