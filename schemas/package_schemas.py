from pydantic import BaseModel
from typing import Optional


class CreatePackageSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    package_type:Optional[str]
    quantity:Optional[int]
    price: Optional[float]
    visible:Optional[bool]

    class Config():
        orm_mode=True
