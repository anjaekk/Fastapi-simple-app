from os import getenv
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql.expression import Update, Delete, Insert
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

env = load_dotenv()
db_for_write = getenv('WRITE_DB_URL')
db_for_read = getenv('READ_DB_URL')
db_for_test = getenv('TEST_DB_URL')
test = getenv('TEST')

engines = {
    'write': create_async_engine(db_for_write),
    'read': create_async_engine(db_for_read),
    'test': create_async_engine(db_for_test),
}

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        print(test)
        if test == False:
            if self._flushing or isinstance(clause, (Update, Delete, Insert)):
                return engines['write'].sync_engine
            else:
                return engines['read'].sync_engine
        else:
           return engines['test'].sync_engine


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
    class_=AsyncSession, sync_session_class=RoutingSession, expire_on_commit=False
    )
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
        


async def create_table():
    async with engines['write'].begin() as conn:
        #await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def connection_dispose():
    for engine in engines.values():
        await engine.dispose()

async def remove(self):
    if self.registry.has(): 
        await self.registry().close() 
    self.registry.clear()