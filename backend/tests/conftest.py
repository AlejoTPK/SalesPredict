import asyncio
from collections.abc import AsyncGenerator
from datetime import datetime, timezone
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infrastructure.db.models.base import Base
from app.main import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture()
async def db_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture()
def app(db_session) -> FastAPI:
    app = create_app()
    app.dependency_overrides[getattr] = db_session  # type: ignore
    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture()
def sample_sale_data() -> dict[str, Any]:
    return {
        "amount": 15000.0,
        "quantity": 5,
        "product_id": "prod-001",
        "product_name": "Enterprise Suite",
        "customer_name": "Acme Corp",
        "region": "North America",
    }


@pytest.fixture()
def sample_user_data() -> dict[str, Any]:
    return {
        "email": "test@salespredict.ai",
        "password": "SecurePass123",
        "full_name": "Test User",
    }
