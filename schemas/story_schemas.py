from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import Optional
from datetime import datetime

class CreateStorySchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    target_group: Optional[str]
    age_from: Optional[int]
    age_to: Optional[int]
    status: Optional[str]
    publish_at: Optional[str]
    days: Optional[int]
    duration: Optional[int]

    class Config:
	    orm_mode=True
