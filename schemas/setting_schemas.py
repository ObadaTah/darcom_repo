from pydantic import BaseModel
from typing import Optional


class CreateSettingSchema(BaseModel):
    key: Optional[str]
    value: Optional[str]
    class Config():
        orm_mode=True
