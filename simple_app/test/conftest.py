import asyncio
from re import S
import pytest_asyncio
import pytest
import json
from os import getenv
import sys
from dotenv import load_dotenv
from graphene.test import Client
from sqlmodel import SQLModel
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from main import graphql_app
from user.serializers import UserAccount
from core.database import engines


env = load_dotenv()
engine_uri = getenv('TEST_DB_URL')
metadata = MetaData()



# @pytest.fixture(scope="session")
# def init_database():
#     return SQLModel.metadata.create_all

# @pytest.fixture(scope="session")
# def engine():
#     engine = create_async_engine(url)
#     yield engine
#     engine.sync_engine.dispose()


# @pytest.fixture(scope="session")
# async def create(engine):
#     close_all_sessions()
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)


# @pytest.fixture
# async def session(engine, create):
#     async with AsyncSession(engine) as session:
#         yield session



















# @pytest.fixture(scope="module")
# def graphql_client():
#     return Client(graphql_app)



import pytest
from asyncio import get_event_loop
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from main import app

engine_uri = 'postgresql+asyncpg://btmttest:btmttest@testdb:55332/btmttest'
_db_conn = create_async_engine(engine_uri)
Base = declarative_base()

# @pytest.fixture(scope="session")
# async def create_table():
#     close_all_sessions()
#     async with _db_conn.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=_db_conn)
    yield
    Base.metadata.drop_all(bind=_db_conn)

@pytest.fixture(scope="session")
async def get_session():
    sess = AsyncSession(bind=_db_conn)
    try:
        yield sess
    finally:
        await sess.close()

# @pytest.fixture(autouse=True, scope="session")
# async def test_db_session():
#     test_async_session = sessionmaker(_db_conn, class_=AsyncSession)
#     try:
#         async with test_async_session() as test_async_session:
#             yield test_async_session
#     finally:
#         await test_async_session.close()

@pytest.fixture(scope="session")
def event_loop():
    loop = get_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()



@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8800") as client:
        yield client










# @pytest_asyncio.fixture(scope="module")
# def test_async_session():
#     engine_for_test = create_async_engine(url)
#     return sessionmaker(engine_for_test, class_=AsyncSession)







# @pytest_asyncio.fixture(scope="session")
# def session
# async_test_session = sessionmaker(
#     class_=AsyncSession, sync_session_class=AsyncSession, expire_on_commit=False
# )

# @pytest_asyncio.fixture(scope="session")
# async def init_database(session):
#     async with session() as session:
# #         await metadata.create_all



# from sqlalchemy.orm.session import close_all_sessions
# @pytest.fixture
# async def input_test_data(test_async_session):
#         user = UserAccount(
#             {
#                 "email":"testeamil@email.com",
#                 "password":"testpassword",
#                 "name":"test"
#             }
#         )
#         test_async_session.add(user)
#         await test_async_session.commit()        
#         # await test_async_session.refresh(user)
#         return test_async_session
        
# from sqlalchemy.sql import select

# @pytest_asyncio.fixture(scope='function')
# async def user(session):
#     user = User(
#         {
#             "email":"testeamil@email.com",
#             "password":"testpassword",
#             "name":"test"
#         }
#     )
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)
#     return user