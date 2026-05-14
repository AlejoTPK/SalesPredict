import asyncio
from datetime import datetime
from app.infrastructure.db.session import async_session_factory
from app.infrastructure.repositories import sale_repo


async def test():
    async with async_session_factory() as db:
        result = await sale_repo.get_aggregated_sales(
            db, start=datetime(2025, 1, 1), end=datetime(2026, 12, 31), group_by="month"
        )
        print(f"Got {len(result)} aggregate rows")
        for row in result[:5]:
            print(row)


asyncio.run(test())
