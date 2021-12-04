from pydantic import BaseModel



class CreatePermissionSchema(BaseModel):
    name: str
    description: str
    key : str

class UpdatePermissionRole(BaseModel):
    role_id: int 
    permission_id: int 