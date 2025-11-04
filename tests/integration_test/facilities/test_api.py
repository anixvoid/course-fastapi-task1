from tests.conftest import async_client

async def test_facilities(async_client):
    response = await async_client.post(
        "/facilities",
        json = {
            "title" : "Аквариум"
        }
    )
    print(f"{response=}")

    assert response.status_code == 200
    assert response.json().get("status") == "OK"

    response = await async_client.get(
        "/facilities"
    )
    print(f"{response=}")

    assert response.status_code == 200
    assert any(map(lambda row: row.get("title") == "Аквариум", response.json()))