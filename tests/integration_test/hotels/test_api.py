from tests.conftest import async_client

async def test_get_hotels(async_client):
    response = await async_client.get(
        "/hotels",
        params = {
            "date_from" : "2024-01-01",
            "date_to"   : "2025-12-31"
        }
    )
    print(f"{response=}")

    assert response.status_code == 200
