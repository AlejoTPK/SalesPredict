import asyncio
from datetime import datetime, timedelta

import pandas as pd

from app.infrastructure.db.session import async_session_factory
from app.tasks import celery_app


async def _run_etl(days_back: int = 90) -> dict:
    """Extract sales from last N days, aggregate into daily metrics."""
    end = datetime.utcnow()
    start = end - timedelta(days=days_back)

    async with async_session_factory() as db:
        from app.infrastructure.repositories.sale_repo import get_sales_by_date_range

        sales = await get_sales_by_date_range(db, start, end)

    if not sales:
        return {"message": "No sales found in range", "count": 0}

    rows = [
        {
            "sale_date": s.sale_date,
            "product_id": s.product_id,
            "region": s.region or "unknown",
            "amount": s.amount,
            "quantity": s.quantity,
        }
        for s in sales
    ]

    df = pd.DataFrame(rows)
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    daily_metrics = (
        df.groupby([pd.Grouper(key="sale_date", freq="D"), "product_id", "region"])
        .agg(
            total_amount=("amount", "sum"),
            total_quantity=("quantity", "sum"),
            transaction_count=("product_id", "count"),
        )
        .reset_index()
    )

    return {
        "message": f"ETL complete: {len(daily_metrics)} daily aggregates from {len(sales)} raw sales",
        "rows_processed": len(sales),
        "aggregates_created": len(daily_metrics),
        "date_range": [start.isoformat(), end.isoformat()],
    }


@celery_app.task(name="run_etl_pipeline")
def run_etl_pipeline(days_back: int = 90) -> dict:
    return asyncio.run(_run_etl(days_back=days_back))
