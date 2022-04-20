import pytest
from os import getenv
from dotenv import load_dotenv
from asyncio import get_event_loop
from asgi_lifespan import LifespanManager
from sqlalchemy import MetaData
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from httpx import AsyncClient

from core.database import get_session
from main import app, router
from user.serializers import UserAccount


env = load_dotenv()
metadata = MetaData()
engine_url = getenv('TEST_DB_URL')
Base = declarative_base()


@pytest.fixture(scope="session")
async def test_engine():
    test_engine = create_async_engine(engine_url)
    if not database_exists:
        await create_database(test_engine.url)
    yield test_engine


@pytest.fixture(scope="session")
async def connection(test_engine):
    connection = test_engine.connect()
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)



async def test_get_session(connection):
    async_session = AsyncSession(bind=connection)
    async with async_session as session:
        yield session
    app.dependency_overrides[get_session] = lambda: session
    # await session.rollback()
    await session.close()
    
app.dependency_overrides[get_session] = lambda: test_get_session


@pytest.fixture(scope="session")
def event_loop():
    loop = get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client() -> AsyncClient:
    app.dependency_overrides[get_session] = lambda: test_get_session
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8800") as client, LifespanManager(app):
        yield client


@pytest.fixture
async def fake_data():
    async for s in test_get_session():
        session = s
    user = UserAccount(
        {
            "email":"testeamil@email.com",
            "password":"testpassword",
            "name":"test"
        }
    )
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user