from sqlalchemy import select, insert, delete

from app.database import async_session_maker


class BaseDAO:
    model = None

    # @classmethod
    # async def get_by_id(cls, model_id):
    #     async with async_session_maker() as session:
    #         query = select(cls.model.__table__.columns).filter_by(id=model_id)
    #         result = await session.execute(query)
    #         return result.mappings().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            # __table__.columns убирает лишний уровень вложенности в mappings
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            # result.all() возвращает кортежи с одним элементом - объектом Booking
            #              другие элементы кортежа могут быть дополнительными запрашиваемыми данными из запроса
            # result.scalars().all() возвращает сразу список объектов Booking
            #                        дополнительных данных здесь видно не будет
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
