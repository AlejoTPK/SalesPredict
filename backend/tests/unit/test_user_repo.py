import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.user_repo import create_user, get_user_by_email, get_user_by_id
from app.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession, sample_user_data):
    user = User(
        email=sample_user_data["email"],
        hashed_password="hashed_placeholder",
        full_name=sample_user_data["full_name"],
    )
    created = await create_user(db_session, user)
    assert created.id is not None
    assert created.email == "test@salespredict.ai"
    assert created.is_active is True


@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession, sample_user_data):
    user = User(
        email=sample_user_data["email"],
        hashed_password="hashed_placeholder",
        full_name=sample_user_data["full_name"],
    )
    await create_user(db_session, user)

    found = await get_user_by_email(db_session, sample_user_data["email"])
    assert found is not None
    assert found.email == sample_user_data["email"]


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(db_session: AsyncSession):
    found = await get_user_by_email(db_session, "nonexistent@test.com")
    assert found is None


@pytest.mark.asyncio
async def test_get_user_by_id(db_session: AsyncSession, sample_user_data):
    user = User(
        email=sample_user_data["email"],
        hashed_password="hashed_placeholder",
        full_name=sample_user_data["full_name"],
    )
    created = await create_user(db_session, user)

    found = await get_user_by_id(db_session, created.id)
    assert found is not None
    assert found.id == created.id
