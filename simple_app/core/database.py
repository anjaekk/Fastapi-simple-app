from os import getenv
from dotenv import load_dotenv

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from sqlalchemy.engine.url import URL


env = load_dotenv()

db_for_write = getenv('WRITE_DB_URL')
db_for_read = getenv('READ_DB_URL')

engine_for_write = create_async_engine(db_for_write , echo=True)
engine_for_read = create_async_engine(db_for_read)

Base = declarative_base()

async_session = sessionmaker(
        engine_for_write, class_=AsyncSession, expire_on_commit=False
    )

# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSession(engine_for_write) as session:
#         yield session



# async def get_session() -> AsyncSession :
#     async_session = sessionmaker(
#         engine_for_write , class_ = AsyncSession , expire_on_commit=False
#     )
#     async with async_session() as session:
#         yield session0

# async def create_table() -> None:
#     async with engine_for_write.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)

# async def get_session() -> AsyncSession:
#     async_session = sessionmaker(
#         engine_for_write, class_=AsyncSession, expire_on_commit=False
#     )
#     try:
#         async with async_session() as session:
#             yield session
#     finally:
#         await session.close()






async def init_models():
    async with engine_for_write.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)