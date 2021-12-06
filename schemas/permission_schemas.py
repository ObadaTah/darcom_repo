from pydantic import BaseModel
from typing import Optional


class CreatePermissionSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    key : Optional[str]

class UpdatePermissionRole(BaseModel):
    role_id: Optional[int] 
    permission_id: Optional[int] 