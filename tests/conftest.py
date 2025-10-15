import pytest

from sqlalchemy.ext.asyncio import create_async_engine

from src.config             import settings
from src.database           import BaseORM, engine_null_pool
from src.models             import *

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)
