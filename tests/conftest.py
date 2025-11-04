import pytest

import json
from httpx                  import AsyncClient, ASGITransport

from src.api.dependencies   import get_db
from src.config             import settings
from src.schemas.hotels     import HotelAdd
from src.schemas.rooms      import RoomAdd

from src.database           import BaseORM, engine_null_pool
from src.models             import *

from src.utils.db_manager   import DBManager
from src.database           import async_session_maker_null_pool

from src.main               import app


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        return db

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)

    mock_hotels = json.load(open("tests/mock_hotels.json", encoding="utf8"))
    mock_rooms  = json.load(open("tests/mock_rooms.json",  encoding="utf8"))

    hotels = [HotelAdd.model_validate(hotel) for hotel in mock_hotels]
    rooms  = [RoomAdd.model_validate(room) for room in mock_rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)

        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://") as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, async_client):
    response = await async_client.post(
        "/auth/register", 
        json = {
            "email"     : "kot@pes.com",
            "password"  : "1234"
        }
    )