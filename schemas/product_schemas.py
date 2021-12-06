from pydantic import BaseModel
from typing import Optional


class CreateProductSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    status: Optional[str]
    tag: Optional[str]
    class Config():
        orm_mode=True
