from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import Optional
from datetime import datetime

class CreateFacilitySchema(BaseModel):
    name: Optional[str]
    user_id: Optional[int]
    owner_name: Optional[str]
    owner_number: Optional[int]
    mobile_number: Optional[int]
    building: Optional[str]
    email: Optional[str]
    floor: Optional[int]
    street: Optional[str]
    balance: Optional[int]
    city_id: Optional[int]
    description: Optional[str]
    notes: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
    instagram_url: Optional[str]
    facebook_url: Optional[str]
    disabled: Optional[bool]
    visible: Optional[bool]
    end_subscription_date: Optional[str]
    name_subscription: Optional[str]
    tag: Optional[str]
    class Config:
	    orm_mode=True


class AddFacilityPhotoSchema(BaseModel):
    tag: Optional[str]