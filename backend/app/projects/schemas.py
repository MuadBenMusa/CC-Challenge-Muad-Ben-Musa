from datetime import date
from typing import Literal

from pydantic import BaseModel
class ProjectRead(BaseModel):
    customer_name: str
    date: date
    task: Literal["cleaning", "inspection", "repair"]
    location: str | None
    description: str | None
    status: Literal["open", "in progress", "done"]

class ProjectCreate(BaseModel):
    customer_id: int
    date: date
    task: Literal["cleaning", "inspection", "repair"]
    location: str | None = None
    description: str | None = None
    status: Literal["open", "in progress", "done"]