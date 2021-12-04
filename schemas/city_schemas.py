from pydantic import BaseModel



class CreateCitySchema(BaseModel):
    name: str
