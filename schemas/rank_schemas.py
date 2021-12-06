from pydantic import BaseModel
from typing import Optional


class CreateRankSchema(BaseModel):
    title: Optional[str]
    points_from: Optional[int]
    points_to: Optional[int]
    class Config():
        orm_mode=True
