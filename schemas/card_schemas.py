from pydantic import BaseModel
from typing import Optional


class CreateCardSchema(BaseModel):
    number: Optional[str]
    price: Optional[int]
    class Config():
        orm_mode=True
