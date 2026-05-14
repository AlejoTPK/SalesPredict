import asyncio
from app.infrastructure.db.session import async_session_factory
from app.infrastructure.repositories import user_repo
from app.core.security import verify_password


async def test():
    async with async_session_factory() as db:
        user = await user_repo.get_user_by_email(db, "demo@salespredict.ai")
        print("User found:", user is not None)
        if user:
            print("Hash prefix:", user.hashed_password[:20])
            result = verify_password("demo123", user.hashed_password)
            print("Verify result:", result)


asyncio.run(test())
