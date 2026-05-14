import asyncio
from app.infrastructure.db.session import async_session_factory
from app.infrastructure.repositories import sale_repo


async def test():
    async with async_session_factory() as db:
        result = await sale_repo.list_sales(db, limit=5)
        print(f"Got {len(result)} sales")
        for sale in result:
            print(f"{sale.id[:8]} - {sale.product_name} - ${sale.amount}")


asyncio.run(test())
