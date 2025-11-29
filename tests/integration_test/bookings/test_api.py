import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-11", 200),
    (1, "2024-08-01", "2024-08-12", 200),
    (1, "2024-08-01", "2024-08-13", 200),
    (1, "2024-08-01", "2024-08-14", 200),
    (1, "2024-08-01", "2024-08-15", 500),
    (1, "2024-08-01", "2024-08-10", 500),
    (1, "2024-08-01", "2024-08-10", 500),
    (1, "2024-08-01", "2024-08-10", 500),
    (1, "2024-08-17", "2024-08-25", 200)
]) 
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db, 
    authenticated_async_client,    
):
    #room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_async_client.post(
        "/bookings",
        json = {
            "room_id"   : room_id,
            "date_from" : date_from,
            "date_to"   : date_to,
        }
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res.get("status") == "OK"
        assert res.get("data")