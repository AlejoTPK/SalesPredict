from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.value_objects.time_range import TimeRange


class Sale(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    amount: float
    quantity: int
    product_id: str
    product_name: str
    customer_id: str | None = None
    customer_name: str | None = None
    region: str | None = None
    status: str = "completed"
    sale_date: TimeRange | None = None
