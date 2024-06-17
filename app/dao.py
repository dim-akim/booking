from sqlalchemy import select, insert

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)  # __table__.columns убирает лишний уровень вложенности в mappings
            result = await session.execute(query)
            # result.all() возвращает кортежи с одним элементом - объектом Booking
            #              другие элементы кортежа могут быть дополнительными запрашиваемыми данными из запроса
            # result.scalars().all() возвращает сразу список объектов Booking
            #                        дополнительных данных здесь видно не будет
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            result = await session.execute(query)
            await session.commit()
            return result
