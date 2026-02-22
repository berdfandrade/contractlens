from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class RefreshToken(BaseModel):
    id: ObjectId | None = Field(default=None, alias="_id")
    user_id: str
    token_hash: str
    created_at: datetime
    expires_at: datetime
    revoked: bool = False
    replaced_by: str | None = None


class RefreshTokenCreate(BaseModel):
    user_id: str
    token_hash: str
    expires_at: datetime


class RefreshTokenPublic(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    revoked: bool
