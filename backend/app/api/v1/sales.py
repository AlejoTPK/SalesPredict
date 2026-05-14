from datetime import datetime

from fastapi import APIRouter, status

from app.api.deps import DbDep
from app.schemas.sale import SaleCreate, SaleResponse
from app.services import sales_service

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(payload: SaleCreate, db: DbDep) -> SaleResponse:
    return await sales_service.create(db, payload)


@router.get("/", response_model=list[SaleResponse])
async def list_sales(db: DbDep, limit: int = 50, offset: int = 0) -> list[SaleResponse]:
    return await sales_service.list_sales(db, limit=limit, offset=offset)


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: str, db: DbDep) -> SaleResponse:
    return await sales_service.get_by_id(db, sale_id)


@router.get("/aggregates/daterange")
async def get_sales_aggregates(
    db: DbDep,
    start_date: datetime,
    end_date: datetime,
    group_by: str = "day",
) -> list[dict]:
    return await sales_service.get_aggregated(db, start_date, end_date, group_by)
