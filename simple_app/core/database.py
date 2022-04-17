from os import getenv
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql.expression import Update, Delete, Insert
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


env = load_dotenv()
db_for_write = getenv('WRITE_DB_URL')
db_for_read = getenv('READ_DB_URL')
Base = declarative_base()
engines = {
    "writer": create_async_engine(db_for_write),
    "reader": create_async_engine(db_for_read),
}

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        else:
            return engines["reader"].sync_engine


async_session = sessionmaker(
    class_=AsyncSession, sync_session_class=RoutingSession, expire_on_commit=False
)

async def get_session():
    sess = async_session
    try:
        yield sess
    finally:
        await sess.close()

async def create_table():
    async with engines["writer"].begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)