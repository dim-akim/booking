from datetime import date

from pydantic import BaseModel

# Для объединения моделей Pydantic и объектов SQLAlchemy есть библиотека SQLModel, чтобы не нарушать DRY


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
