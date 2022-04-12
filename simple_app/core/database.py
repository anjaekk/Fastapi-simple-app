from os import getenv
from dotenv import load_dotenv

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


env = load_dotenv()


engine_for_write = create_async_engine(
    getenv('WRITE_DB_URL'), encoding='utf8', convert_unicode=True, echo=True
)
engine_for_read = create_async_engine(
    getenv('READ_DB_URL'), encoding='utf8', convert_unicode=True
)

Base = declarative_base()

async_session = sessionmaker(
        engine_for_write, class_=AsyncSession, expire_on_commit=False
    )
async def get_session() -> AsyncSession:
    try:
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
    finally:
        await session.close()


async def create_table() -> None:
    async with engine_for_write.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)