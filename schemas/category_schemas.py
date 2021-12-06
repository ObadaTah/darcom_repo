from pydantic import BaseModel
from typing import Optional


class CreateCategorySchema(BaseModel):
    title: Optional[str]
    parent_id: Optional[int]
