import pytest
from httpx                  import AsyncClient, ASGITransport

from src.config             import settings
from src.database           import BaseORM, engine_null_pool
from src.models             import *

from src.main               import app

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://") as ac:
        response = await ac.post(
            "/auth/register", 
            json = {
                "email"     : "kot@pes.com",
                "password"  : "1234"
            }
        )