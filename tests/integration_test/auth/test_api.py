from tests.conftest import test_account, authenticated_async_client

async def test_auth(authenticated_async_client):
    response = await authenticated_async_client.get(
        "/auth/me"
    )

    assert response.status_code == 200
    assert response.json().get("email") == test_account["email"]
