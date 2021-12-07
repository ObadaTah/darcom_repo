from pydantic import BaseModel
from typing import Optional


class CreateMessageSchema(BaseModel):
    messageable_id: Optional[int]
    messageable_type: Optional[str]
    message_title: Optional[str]
    message_description: Optional[str]
    message_rate: Optional[int]
    message_audience: Optional[str]
    message_reaction: Optional[str]
    message_status: Optional[str]
    class Config():
        orm_mode=True
