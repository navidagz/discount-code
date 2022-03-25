from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import async_session


async def db_session() -> AsyncSession:
    """
    Dependency function that yields db session
    """
    async with async_session() as session:
        yield session
        await session.commit()
