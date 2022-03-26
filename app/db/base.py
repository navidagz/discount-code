from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

engine = create_async_engine(settings.async_database_url, echo=settings.DB_ECHO_LOG)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    @staticmethod
    def build_where(model_class, query, data: Dict):
        for k, v in data.items():
            query = query.where(getattr(model_class, k) == v)
        return query

    @classmethod
    async def get_or_create(cls, session: AsyncSession, **kwargs):
        q = select(cls)
        q = cls.build_where(cls, q, kwargs)

        instance = (await session.execute(q)).scalar()

        if instance:
            return instance, False
        else:
            instance = cls(**kwargs)
            try:
                session.add(instance)
                await session.flush()
                await session.refresh(instance)
            except Exception:
                await session.rollback()
                return instance, False
            else:
                return instance, True

    @classmethod
    async def get_by_filter(cls, session: AsyncSession, query_filter: Dict):  # pragma: no cover
        q = select(cls)
        q = cls.build_where(cls, q, query_filter)
        return (await session.execute(q)).scalar()

    async def update_record(self, session: AsyncSession, data: Dict):
        for k, v in data.items():
            setattr(self, k, v)

        await session.flush()
