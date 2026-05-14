from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SaleCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    amount: float = Field(gt=0)
    quantity: int = Field(gt=0)
    product_id: str
    product_name: str
    customer_id: str | None = None
    customer_name: str | None = None
    region: str | None = None


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    amount: float
    quantity: int
    product_id: str
    product_name: str
    customer_id: str | None = None
    customer_name: str | None = None
    region: str | None = None
    status: str
    sale_date: datetime | None = None
