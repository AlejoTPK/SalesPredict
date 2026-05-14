import asyncio
from app.infrastructure.db.session import engine
from sqlalchemy import text


async def test():
    print("Starting connection...")
    async with engine.connect() as conn:
        print("Connected")
        result = await conn.execute(text("SELECT 1"))
        print("Result:", result.scalar())
    print("Done")


asyncio.run(test())
