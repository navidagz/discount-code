import asyncio
from datetime import timedelta
from typing import AsyncGenerator, Generator, Callable

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.db.base import async_session, engine
from app.utils.datetime_utils import current_datetime


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """
    Create an instance of the default event loop for each test case.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture(scope='function')
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture(scope='function')
def app(override_get_db: Callable) -> FastAPI:
    from app.dependencies.db import db_session
    from app.main import app

    app.dependency_overrides[db_session()] = override_get_db
    return app


@pytest_asyncio.fixture(scope='function')
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def current_time_string():
    yield (current_datetime() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
