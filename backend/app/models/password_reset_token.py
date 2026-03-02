from pydantic import BaseModel
from datetime import datetime


class PasswordResetToken(BaseModel):
    user_id: str
    token_hash: str
    created_at: datetime
    expires_at: datetime
