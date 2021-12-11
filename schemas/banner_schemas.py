from pydantic import BaseModel
from typing import Optional

class CreateBannerSchema(BaseModel):
    banner_type: Optional[str]
    facility_id: Optional[int]
    city_id: Optional[int]
    start_at: Optional[str]
    end_at: Optional[str]
    url: Optional[str]
    status: Optional[str]