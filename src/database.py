import asyncio

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings 

#print(settings.DB_URL)
engine = create_async_engine(settings.DB_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class BaseORM(DeclarativeBase):
    pass

async def func(): #demo engine
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(res.fetchone())


async def func2(): #demo async_session_maker
    async with async_session_maker.begin() as session:
        await session.execute()

#asyncio.run(func())
