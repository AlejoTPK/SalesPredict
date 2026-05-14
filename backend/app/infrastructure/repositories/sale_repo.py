from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.sale import Sale
from app.infrastructure.db.session import engine


async def create_sale(db: AsyncSession, sale: Sale) -> Sale:
    db.add(sale)
    await db.flush()
    await db.refresh(sale)
    return sale


async def get_sale_by_id(db: AsyncSession, sale_id: str) -> Sale | None:
    result = await db.execute(select(Sale).where(Sale.id == sale_id))
    return result.scalar_one_or_none()


async def list_sales(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Sale]:
    result = await db.execute(
        select(Sale).order_by(Sale.sale_date.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all())


async def get_sales_by_date_range(
    db: AsyncSession,
    start: datetime,
    end: datetime,
) -> list[Sale]:
    result = await db.execute(
        select(Sale)
        .where(Sale.sale_date >= start, Sale.sale_date <= end)
        .order_by(Sale.sale_date.asc())
    )
    return list(result.scalars().all())


async def get_aggregated_sales(
    db: AsyncSession,
    start: datetime,
    end: datetime,
    group_by: str = "day",
) -> list[dict]:
    if engine.dialect.name == "sqlite":
        fmt = {"day": "%Y-%m-%d", "week": "%Y-%W", "month": "%Y-%m"}.get(group_by, "%Y-%m-%d")
        date_col = func.strftime(fmt, Sale.sale_date)
    else:
        date_col = func.date_trunc(group_by, Sale.sale_date)

    result = await db.execute(
        select(
            date_col.label("period"),
            func.sum(Sale.amount).label("total_amount"),
            func.sum(Sale.quantity).label("total_quantity"),
            func.count(Sale.id).label("count"),
        )
        .where(Sale.sale_date >= start, Sale.sale_date <= end)
        .group_by(date_col)
        .order_by(date_col)
    )
    rows = result.all()
    return [
        {"period": row[0], "total_amount": row[1], "total_quantity": row[2], "count": row[3]}
        for row in rows
    ]


async def get_product_sales_breakdown(
    db: AsyncSession,
    start: datetime,
    end: datetime,
) -> list[dict]:
    result = await db.execute(
        select(
            Sale.product_id,
            Sale.product_name,
            func.sum(Sale.amount).label("total_amount"),
            func.sum(Sale.quantity).label("total_quantity"),
            func.count(Sale.id).label("sale_count"),
        )
        .where(Sale.sale_date >= start, Sale.sale_date <= end)
        .group_by(Sale.product_id, Sale.product_name)
        .order_by(func.sum(Sale.amount).desc())
    )
    rows = result.all()
    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "total_amount": row[2],
            "total_quantity": row[3],
            "sale_count": row[4],
        }
        for row in rows
    ]


async def get_product_timeline(
    db: AsyncSession,
    product_id: str,
    start: datetime,
    end: datetime,
) -> list[dict]:
    if engine.dialect.name == "sqlite":
        date_col = func.strftime("%Y-%m-%d", Sale.sale_date)
    else:
        date_col = func.date_trunc("day", Sale.sale_date)

    result = await db.execute(
        select(
            date_col.label("period"),
            func.sum(Sale.amount).label("daily_amount"),
            func.sum(Sale.quantity).label("daily_quantity"),
        )
        .where(
            Sale.product_id == product_id,
            Sale.sale_date >= start,
            Sale.sale_date <= end,
        )
        .group_by(date_col)
        .order_by(date_col)
    )
    rows = result.all()
    return [
        {"period": str(row[0]), "daily_amount": row[1], "daily_quantity": row[2]} for row in rows
    ]


async def get_distinct_products(db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(Sale.product_id, Sale.product_name)
        .distinct(Sale.product_id)
        .order_by(Sale.product_name)
    )
    rows = result.all()
    return [{"product_id": row[0], "product_name": row[1]} for row in rows]
