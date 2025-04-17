from typing import Union

from sqlalchemy import text
from sqlalchemy import Select, Insert, Update, Delete
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings 

#print(settings.DB_URL)

engine = create_async_engine(settings.DB_URL)#, echo=True)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class BaseORM(DeclarativeBase):
    pass

def sprint(stmt: Union[Select, Insert, Update, Delete]): 
    """Формирование и печать RAW SQL запроса"""
    print(stmt.compile(
        engine,
        compile_kwargs = {
            "literal_binds": True
        }
    ))

async def func(): #demo engine
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(res.fetchone())


async def func2(): #demo async_session_maker
    async with async_session_maker.begin() as session:
        await session.execute()

#asyncio.run(func())
