from tests.conftest import async_client

async def test_post_facilities(async_client):
    facility_title = "Массаж"
    response = await async_client.post(
        "/facilities",
        json = {
            "title" : facility_title
        }
    )
    assert response.status_code == 200

    res = response.json()    
    assert isinstance(res, dict)
    assert res.get("status") == "OK"
    assert res["data"]["title"]  == facility_title

async def test_get_facilities(async_client):
    response = await async_client.get(
        "/facilities"
    )
    print(f"{response=}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)