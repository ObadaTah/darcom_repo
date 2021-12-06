from pydantic import BaseModel
from typing import Optional

class CreateBannerSchema(BaseModel):
    banner_type: Optional[str]
    start_at: Optional[str]
    end_at: Optional[str]
    url: Optional[str]
    status: Optional[str]