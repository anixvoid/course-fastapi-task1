from typing import Literal
from httpx import AsyncClient
import pytest

from tests.conftest import test_account, authenticated_async_client


async def test_auth(authenticated_async_client):
    response = await authenticated_async_client.get("/auth/me")

    assert response.status_code == 200
    assert response.json().get("email") == test_account["email"]


@pytest.mark.parametrize(
    "email, password, result",
    [
        ("user1@mail.com", "pa$$word1", 200),
        ("user2@mail.com", "pa$$word2", 200),
        ("user3@mail.com", "pa$$word3", 200),
        ("error@error", "pa$$word4", 422),
        ("error", "pa$$word5", 422),
    ],
)
async def test_register_user(email: str, password: str, result: int, async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register", json={"email": email, "password": password}
    )

    assert response.status_code == result


@pytest.mark.parametrize(
    "email, password, result",
    [
        ("user1@mail.com", "pa$$word1", 200),
        ("user2@mail.com", "error", 401),
        ("error@mail.com", "pa$$word3", 401),
        ("error@error", "pa$$word4", 422),
        ("error", "pa$$word5", 422),
    ],
)
async def test_auth_flow(email: str, password: str, result: str, async_client: AsyncClient):
    resp_login = await async_client.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == result
    if resp_login.status_code == 200:
        assert resp_login.json().get("access_token")
        assert async_client.cookies.get("access_token")

        resp_me = await async_client.get("/auth/me")
        assert resp_me.status_code == 200
        assert resp_me.json().get("email") == email

        resp_logout = await async_client.post("/auth/logout", json=test_account)
        assert resp_logout.status_code == 200
        assert resp_logout.json().get("status") == "OK"
        assert "access_token" not in async_client.cookies

    resp_me2 = await async_client.get("/auth/me")
    assert resp_me2.status_code == 401
