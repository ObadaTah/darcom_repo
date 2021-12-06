from pydantic import BaseModel
from typing import Optional


class CreatePurchaseSchema(BaseModel):
    customer_name: Optional[str]
    customer_mobile: Optional[str]
    customer_address: Optional[str]
    info: Optional[str]
    quantity: Optional[int]
    status: Optional[str]
    class Config():
        orm_mode=True
