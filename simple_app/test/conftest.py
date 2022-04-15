# import pytest
from graphene.test import Client
# import pytest_asyncio
# from sqlalchemy.ext.asyncio import create_async_engine





# # @pytest.fixture(scope="session")
# # def database_url():
# #     return "postgresql+asyncpg://postgres:masterkey@localhost/dbtest"







# import pytest
# import sqlalchemy as sa
# from sqlalchemy import orm
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Base = orm.declarative_base()

# # @pytest.fixture(scope="session")
# # def engine():
# #     engine = create_async_engine(
# #         "postgresql+asyncpg://postgres:masterkey@localhost/dbtest"
# #     )
# #     yield engine
# #     engine.sync_engine.dispose()
# # @pytest.fixture(autouse=True) 
# # def setup_database():
# #     database = "postgresql+asyncpg://postgres:masterkey@localhost/dbtest"




# # @pytest.fixture
# # async def session(engine, create):
# #     async with AsyncSession(engine) as session:
# #         yield session
        




# import pytest

from sqlalchemy import MetaData, Table, String, Integer, Column
from user.serializers import User
metadata = MetaData()


# @pytest.fixture()
# async def create(engine):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)




# @pytest.fixture(scope="function")
# def user():
#     user = User()
import sys
import os
import asyncio
import pytest
from sqlalchemy import create_mock_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from os import getenv
from dotenv import load_dotenv
from main import graphql_app
env = load_dotenv()
url = getenv('WRITE_DB_URL')
from core.database import async_session

import aiohttp
from aiographql.client import GraphQLClient

from aiographql.client.helpers import aiohttp_client_session


db = async_session()

@pytest.fixture(scope="module")
def graphql_client():
    return Client(graphql_app)



# @pytest.fixture(autouse=True)
# async def get_session():
#     engine_for_test = create_async_engine(url)
#     test_async_session = sessionmaker(engine_for_test, class_=AsyncSession)
#     try:
#         async with test_async_session() as test_async_session:
#             yield test_async_session
#     finally:
#         await test_async_session.close()



# @pytest.fixture(autouse=True)
# def graphql_client(get_session):
#     engine_for_test = create_async_engine(url)
#     client = GraphQLClient(
#     endpoint="http://127.0.0.1:8080/graphql",
#     session = aiohttp_client_session
#     # session=session,
#     )
#     return client
    



# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()

# @pytest.fixture(scope="session")
# async def init_database(session):
#     async with session() as session:
#         await metadata.create_all


# async def init_test_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope='function')
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
