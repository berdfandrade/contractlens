from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from bson import ObjectId

class UserCreate(BaseModel):
    name : str
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    id: Optional[ObjectId] = None
    email: str
    password: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
