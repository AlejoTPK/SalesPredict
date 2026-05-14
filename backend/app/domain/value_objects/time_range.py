from datetime import datetime

from pydantic import BaseModel


class TimeRange(BaseModel):
    start: datetime
    end: datetime
