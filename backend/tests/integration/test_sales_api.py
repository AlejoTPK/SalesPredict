import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, sample_user_data):
    response = await client.post("/api/v1/auth/register", json=sample_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, sample_user_data):
    await client.post("/api/v1/auth/register", json=sample_user_data)
    response = await client.post("/api/v1/auth/register", json=sample_user_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, sample_user_data):
    await client.post("/api/v1/auth/register", json=sample_user_data)
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": sample_user_data["email"], "password": sample_user_data["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@test.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_sales_empty(client: AsyncClient):
    response = await client.get("/api/v1/sales")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_sale(client: AsyncClient, sample_sale_data):
    response = await client.post("/api/v1/sales", json=sample_sale_data)
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == sample_sale_data["product_name"]
    assert data["amount"] == sample_sale_data["amount"]
