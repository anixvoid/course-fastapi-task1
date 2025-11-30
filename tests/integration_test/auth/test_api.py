import pytest

from tests.conftest import test_account, authenticated_async_client

async def test_auth(authenticated_async_client):
    response = await authenticated_async_client.get(
        "/auth/me"
    )

    assert response.status_code == 200
    assert response.json().get("email") == test_account["email"]

@pytest.mark.parametrize("email, password", [
    ("user1@mail.com", "pa$$word1"),
    ("user2@mail.com", "pa$$word2"),
    ("user3@mail.com", "pa$$word3"),
])
async def test_register_user(
    email,
    password,
    async_client
):
    response = await async_client.post(
        "/auth/register", 
        json = {
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200

@pytest.mark.parametrize("email, password, result", [
    ("user1@mail.com", "pa$$word1",    200),
    ("user2@mail.com", "error",        401),
    ("error@mail.com", "pa$$word3",    401),
])
async def test_auth_login_logout_user(
    email,
    password,
    result,
    async_client
):    
    response = await async_client.post(
        "/auth/login", 
        json = {
            "email":    email,
            "password": password
        }
    )

    assert response.status_code == result
    if response.status_code == 200:
        assert response.json().get("access_token")
        assert async_client.cookies.get("access_token")

        response = await async_client.get(
            "/auth/me"
        )

        assert response.status_code == 200
        assert response.json().get("email") == email

        response = await async_client.post(
            "/auth/logout", 
            json = test_account
        )
        assert response.status_code == 200
        assert response.json().get("status") == "OK"

    response = await async_client.get(
        "/auth/me"
    )
    assert response.status_code == 401