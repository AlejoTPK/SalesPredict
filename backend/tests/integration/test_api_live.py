import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import create_app
from app.infrastructure.db.session import async_session_factory
from app.infrastructure.db.models.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.repositories import user_repo
from app.core.security import hash_password
from app.infrastructure.db.models.user import User


@pytest.fixture(scope="module")
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def demo_user():
    async with async_session_factory() as db:
        user = User(
            email="demo@salespredict.ai",
            hashed_password=hash_password("demo123"),
            full_name="Demo User",
        )
        db.add(user)
        await db.commit()
        return user


@pytest.mark.asyncio
async def test_login(client: TestClient, demo_user):
    resp = client.post(
        "/api/v1/auth/login",
        json={
            "email": "demo@salespredict.ai",
            "password": "demo123",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    print(f"Token received: {data['access_token'][:20]}...")


@pytest.mark.asyncio
async def test_sales_list_empty(client: TestClient):
    resp = client.get("/api/v1/sales?limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
