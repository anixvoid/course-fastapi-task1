import pytest

from sqlalchemy.ext.asyncio import create_async_engine

from src.config             import settings
from src.database           import BaseORM, engine_null_pool
from src.models             import *

@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)
