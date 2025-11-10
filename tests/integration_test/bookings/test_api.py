async def test_add_booking(db, authenticated_async_client):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_async_client.post(
        "/bookings",
        json = {
            "room_id": room_id,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res.get("status") == "OK"
    assert res.get("data")