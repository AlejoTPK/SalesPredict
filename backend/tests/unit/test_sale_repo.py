import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.sale_repo import (
    create_sale,
    get_aggregated_sales,
    get_sale_by_id,
    get_sales_by_date_range,
    list_sales,
)
from app.infrastructure.db.models.sale import Sale


@pytest.mark.asyncio
async def test_create_sale(db_session: AsyncSession, sample_sale_data):
    sale = Sale(
        amount=sample_sale_data["amount"],
        quantity=sample_sale_data["quantity"],
        product_id=sample_sale_data["product_id"],
        product_name=sample_sale_data["product_name"],
        customer_name=sample_sale_data["customer_name"],
        region=sample_sale_data["region"],
        sale_date=__import__("datetime").datetime.utcnow(),
    )
    created = await create_sale(db_session, sale)

    assert created.id is not None
    assert created.amount == 15000.0
    assert created.status == "completed"


@pytest.mark.asyncio
async def test_get_sale_by_id(db_session: AsyncSession, sample_sale_data):
    sale = Sale(
        amount=sample_sale_data["amount"],
        quantity=sample_sale_data["quantity"],
        product_id=sample_sale_data["product_id"],
        product_name=sample_sale_data["product_name"],
        sale_date=__import__("datetime").datetime.utcnow(),
    )
    created = await create_sale(db_session, sale)

    found = await get_sale_by_id(db_session, created.id)
    assert found is not None
    assert found.id == created.id


@pytest.mark.asyncio
async def test_get_sale_not_found(db_session: AsyncSession):
    found = await get_sale_by_id(db_session, "non-existent-id")
    assert found is None


@pytest.mark.asyncio
async def test_list_sales(db_session: AsyncSession, sample_sale_data):
    for i in range(3):
        sale = Sale(
            amount=sample_sale_data["amount"] + i * 100,
            quantity=sample_sale_data["quantity"],
            product_id=f"prod-{i}",
            product_name=sample_sale_data["product_name"],
            sale_date=__import__("datetime").datetime.utcnow(),
        )
        await create_sale(db_session, sale)

    sales = await list_sales(db_session, limit=10, offset=0)
    assert len(sales) == 3


@pytest.mark.asyncio
async def test_get_aggregated_sales(db_session: AsyncSession, sample_sale_data):
    dt = __import__("datetime").datetime
    sale = Sale(
        amount=sample_sale_data["amount"],
        quantity=sample_sale_data["quantity"],
        product_id=sample_sale_data["product_id"],
        product_name=sample_sale_data["product_name"],
        sale_date=dt.utcnow(),
    )
    await create_sale(db_session, sale)

    now = dt.utcnow()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now

    result = await get_aggregated_sales(db_session, start, end, group_by="day")
    assert len(result) > 0
    assert "period" in result[0]
    assert "total_amount" in result[0]
