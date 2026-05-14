from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.infrastructure.db.models.sale import Sale
from app.infrastructure.repositories import sale_repo
from app.schemas.sale import SaleCreate, SaleResponse


async def create(db: AsyncSession, payload: SaleCreate) -> SaleResponse:
    sale = Sale(
        amount=payload.amount,
        quantity=payload.quantity,
        product_id=payload.product_id,
        product_name=payload.product_name,
        customer_id=payload.customer_id,
        customer_name=payload.customer_name,
        region=payload.region,
        sale_date=datetime.utcnow(),
    )
    sale = await sale_repo.create_sale(db, sale)
    return SaleResponse.model_validate(sale)


async def get_by_id(db: AsyncSession, sale_id: str) -> SaleResponse:
    sale = await sale_repo.get_sale_by_id(db, sale_id)
    if sale is None:
        raise NotFoundError("Sale not found")
    return SaleResponse.model_validate(sale)


async def list_sales(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[SaleResponse]:
    sales = await sale_repo.list_sales(db, limit=limit, offset=offset)
    return [SaleResponse.model_validate(s) for s in sales]


async def get_aggregated(
    db: AsyncSession,
    start: datetime,
    end: datetime,
    group_by: str = "day",
) -> list[dict]:
    return await sale_repo.get_aggregated_sales(db, start, end, group_by)
