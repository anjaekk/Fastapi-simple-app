import asyncio
import pytest_asyncio
from os import getenv
from dotenv import load_dotenv
from graphene.test import Client
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from main import graphql_app
from user.serializers import User


env = load_dotenv()
url = getenv('WRITE_DB_URL')
metadata = MetaData()


@pytest_asyncio.fixture(scope="module")
def graphql_client():
    return Client(graphql_app)


@pytest_asyncio.fixture(autouse=True)
async def get_session():
    engine_for_test = create_async_engine(url)
    test_async_session = sessionmaker(engine_for_test, class_=AsyncSession)
    try:
        async with test_async_session() as test_async_session:
            yield test_async_session
    finally:
        await test_async_session.close()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def init_database(session):
    async with session() as session:
        await metadata.create_all


@pytest_asyncio.fixture(scope='function')
async def user(session):
    user = User(
        {
            "email":"testeamil@email.com",
            "password":"testpassword",
            "name":"test"
        }
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user