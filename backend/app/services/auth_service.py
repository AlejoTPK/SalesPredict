from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.infrastructure.db.models.user import User
from app.infrastructure.repositories import user_repo
from app.schemas.auth import UserCreate, UserResponse


async def register_user(db: AsyncSession, payload: UserCreate) -> UserResponse:
    existing = await user_repo.get_user_by_email(db, payload.email)
    if existing:
        raise ConflictError("Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )
    user = await user_repo.create_user(db, user)
    return UserResponse.model_validate(user)


async def get_user(db: AsyncSession, user_id: str) -> UserResponse:
    user = await user_repo.get_user_by_id(db, user_id)
    if user is None:
        raise NotFoundError("User not found")
    return UserResponse.model_validate(user)
