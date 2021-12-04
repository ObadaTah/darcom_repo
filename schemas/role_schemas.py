from pydantic import BaseModel



class CreateRoleSchema(BaseModel):
    name: str
    description: str

class UpdateUsersRole(BaseModel):
    role_id: int 
    user_id: int 