from pydantic import BaseModel
from typing import Optional


class CreateCommentSchema(BaseModel):
    commentable_id: Optional[int]
    commentable_type: Optional[str]
    comment_text: Optional[str]
    comment_rate: Optional[int]
    comment_status: Optional[str]
    class Config():
        orm_mode=True
