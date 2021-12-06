from pydantic import BaseModel
from typing import Optional


class CreateSubscriptionSchema(BaseModel):
    title: Optional[str]
    visible:Optional[bool]
    title: Optional[str]
    number_of_months:Optional[int]
    cost:Optional[float]
    number_of_stories:Optional[int]
    number_of_ad_text:Optional[int]
    

    class Config():
        orm_mode=True
