from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel


class CurrentTicker(BaseModel):
    # id: Optional[UUID] = uuid4()
    current_ticker: str


class UpdateTicker(BaseModel):
    # id=UUID("5cd1e186-1d4a-4378-91fc-bea9f58b4cfa")
    new_ticker: str

